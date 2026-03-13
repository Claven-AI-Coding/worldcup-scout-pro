"""合规管理 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.compliance import (
    BannedWordBatchCreate,
    BannedWordCreate,
    BannedWordResponse,
    ContentCheckRequest,
    ContentCheckResponse,
    ReportCreate,
    ReportResponse,
    ReportReview,
    UserViolationCreate,
    UserViolationResponse,
)
from app.services.compliance_service import ComplianceService
from app.utils.auth import get_current_user, require_admin
from app.utils.content_filter import filter_content

router = APIRouter(prefix="/compliance", tags=["compliance"])


# ============ 违禁词管理（管理员）============
@router.post(
    "/banned-words",
    response_model=BannedWordResponse,
    dependencies=[Depends(require_admin)],
)
async def add_banned_word(
    data: BannedWordCreate, db: AsyncSession = Depends(get_db)
):
    """添加违禁词（管理员）"""
    service = ComplianceService(db)
    word = await service.add_banned_word(data)
    return word


@router.post(
    "/banned-words/batch",
    dependencies=[Depends(require_admin)],
)
async def add_banned_words_batch(
    data: BannedWordBatchCreate, db: AsyncSession = Depends(get_db)
):
    """批量添加违禁词（管理员）"""
    service = ComplianceService(db)
    count = await service.add_banned_words_batch(data.words, data.category)
    return {"added_count": count, "total_submitted": len(data.words)}


@router.get(
    "/banned-words",
    response_model=list[BannedWordResponse],
    dependencies=[Depends(require_admin)],
)
async def get_banned_words(
    category: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """获取违禁词列表（管理员）"""
    service = ComplianceService(db)
    words = await service.get_banned_words(category, skip, limit)
    return words


@router.delete(
    "/banned-words/{word_id}",
    dependencies=[Depends(require_admin)],
)
async def delete_banned_word(word_id: int, db: AsyncSession = Depends(get_db)):
    """删除违禁词（管理员）"""
    service = ComplianceService(db)
    success = await service.delete_banned_word(word_id)
    if not success:
        raise HTTPException(status_code=404, detail="Banned word not found")
    return {"message": "Banned word deleted"}


# ============ 举报管理 ============
@router.post("/reports", response_model=ReportResponse)
async def create_report(
    data: ReportCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建举报"""
    service = ComplianceService(db)
    report = await service.create_report(current_user.id, data)
    return report


@router.get(
    "/reports/pending",
    response_model=list[ReportResponse],
    dependencies=[Depends(require_admin)],
)
async def get_pending_reports(
    skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    """获取待审核举报（管理员）"""
    service = ComplianceService(db)
    reports = await service.get_pending_reports(skip, limit)
    return reports


@router.post(
    "/reports/{report_id}/review",
    response_model=ReportResponse,
    dependencies=[Depends(require_admin)],
)
async def review_report(
    report_id: int, review: ReportReview, db: AsyncSession = Depends(get_db)
):
    """审核举报（管理员）"""
    service = ComplianceService(db)
    report = await service.review_report(report_id, review)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


# ============ 用户违规管理（管理员）============
@router.post(
    "/violations",
    response_model=UserViolationResponse,
    dependencies=[Depends(require_admin)],
)
async def create_violation(
    data: UserViolationCreate, db: AsyncSession = Depends(get_db)
):
    """创建违规记录（管理员）"""
    service = ComplianceService(db)
    violation = await service.create_violation(data)
    return violation


@router.get("/violations/user/{user_id}", response_model=list[UserViolationResponse])
async def get_user_violations(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取用户违规记录（本人或管理员）"""
    # 只能查看自己的或管理员查看所有
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    service = ComplianceService(db)
    violations = await service.get_user_violations(user_id, skip, limit)
    return violations


@router.get("/ban-status/{user_id}")
async def check_ban_status(user_id: int, db: AsyncSession = Depends(get_db)):
    """检查用户封禁状态（公开）"""
    service = ComplianceService(db)
    status_info = await service.check_user_ban_status(user_id)
    return status_info


# ============ 内容检查工具 ============
@router.post("/check-content", response_model=ContentCheckResponse)
async def check_content_api(
    data: ContentCheckRequest, db: AsyncSession = Depends(get_db)
):
    """检查内容是否包含违禁词（公开，用于前端实时检查）"""
    service = ComplianceService(db)
    result = await service.check_text_content(data.text)

    # 同时返回过滤后的文本
    filtered = await filter_content(data.text, db)

    return {
        "is_clean": result["is_clean"],
        "matched_words": result["matched_words"],
        "categories": result["categories"],
        "filtered_text": filtered if not result["is_clean"] else None,
    }

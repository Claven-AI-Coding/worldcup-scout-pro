"""合规管理服务层"""

from datetime import datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banned_word import BannedWord
from app.models.post import Post
from app.models.report import Report
from app.models.user import User
from app.models.user_violation import UserViolation
from app.schemas.compliance import (
    BannedWordCreate,
    ReportCreate,
    ReportReview,
    UserViolationCreate,
)
from app.utils.content_filter import check_content, reset_cache


class ComplianceService:
    """合规管理服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ============ 违禁词管理 ============
    async def add_banned_word(self, data: BannedWordCreate) -> BannedWord:
        """添加违禁词"""
        word = BannedWord(word=data.word, category=data.category)
        self.db.add(word)
        await self.db.commit()
        await self.db.refresh(word)
        reset_cache()  # 重置缓存
        return word

    async def add_banned_words_batch(self, words: list[str], category: str | None = None) -> int:
        """批量添加违禁词"""
        existing = await self.db.execute(select(BannedWord.word).where(BannedWord.word.in_(words)))
        existing_words = {w for (w,) in existing.all()}

        new_words = [
            BannedWord(word=w, category=category) for w in words if w not in existing_words
        ]

        if new_words:
            self.db.add_all(new_words)
            await self.db.commit()
            reset_cache()

        return len(new_words)

    async def get_banned_words(
        self, category: str | None = None, skip: int = 0, limit: int = 100
    ) -> list[BannedWord]:
        """获取违禁词列表"""
        query = select(BannedWord)
        if category:
            query = query.where(BannedWord.category == category)
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete_banned_word(self, word_id: int) -> bool:
        """删除违禁词"""
        result = await self.db.execute(delete(BannedWord).where(BannedWord.id == word_id))
        await self.db.commit()
        if result.rowcount > 0:
            reset_cache()
            return True
        return False

    # ============ 举报管理 ============
    async def create_report(self, reporter_id: int, data: ReportCreate) -> Report:
        """创建举报"""
        report = Report(
            reporter_id=reporter_id,
            target_type=data.target_type,
            target_id=data.target_id,
            reason=data.reason,
        )
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def get_pending_reports(self, skip: int = 0, limit: int = 50) -> list[Report]:
        """获取待审核举报"""
        result = await self.db.execute(
            select(Report)
            .where(Report.status == "pending")
            .order_by(Report.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def review_report(self, report_id: int, review: ReportReview) -> Report | None:
        """审核举报"""
        result = await self.db.execute(select(Report).where(Report.id == report_id))
        report = result.scalar_one_or_none()
        if not report:
            return None

        report.status = review.status
        report.reviewed_at = datetime.utcnow()

        # 执行处理动作
        if review.action and review.status == "reviewed":
            await self._execute_action(
                report.target_type,
                report.target_id,
                review.action,
                review.ban_days,
                review.notes,
            )

        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def _execute_action(
        self,
        target_type: str,
        target_id: int,
        action: str,
        ban_days: int | None,
        notes: str | None,
    ) -> None:
        """执行处理动作"""
        if action == "delete_content" and target_type == "post":
            # 删除帖子
            await self.db.execute(delete(Post).where(Post.id == target_id))

        elif action in ("warn_user", "ban_user"):
            # 获取用户 ID
            user_id = await self._get_user_id_from_target(target_type, target_id)
            if user_id:
                # 创建违规记录
                violation = UserViolation(
                    user_id=user_id,
                    violation_type="reported",
                    severity="serious" if action == "ban_user" else "warning",
                    action_taken="temp_ban" if ban_days else "warned",
                    ban_until=(datetime.utcnow() + timedelta(days=ban_days) if ban_days else None),
                    notes=notes,
                )
                self.db.add(violation)

                # 如果是封禁，更新用户状态
                if action == "ban_user" and ban_days:
                    user_result = await self.db.execute(select(User).where(User.id == user_id))
                    user = user_result.scalar_one_or_none()
                    if user:
                        user.is_banned = True
                        user.ban_until = datetime.utcnow() + timedelta(days=ban_days)

    async def _get_user_id_from_target(self, target_type: str, target_id: int) -> int | None:
        """从目标获取用户 ID"""
        if target_type == "user":
            return target_id
        elif target_type == "post":
            result = await self.db.execute(select(Post.author_id).where(Post.id == target_id))
            return result.scalar_one_or_none()
        return None

    # ============ 用户违规管理 ============
    async def create_violation(self, data: UserViolationCreate) -> UserViolation:
        """创建违规记录"""
        ban_until = None
        if data.ban_days:
            ban_until = datetime.utcnow() + timedelta(days=data.ban_days)

        violation = UserViolation(
            user_id=data.user_id,
            violation_type=data.violation_type,
            severity=data.severity,
            content=data.content,
            action_taken=data.action_taken,
            ban_until=ban_until,
            notes=data.notes,
        )
        self.db.add(violation)

        # 如果是封禁，更新用户状态
        if data.action_taken in ("temp_ban", "permanent_ban"):
            user_result = await self.db.execute(select(User).where(User.id == data.user_id))
            user = user_result.scalar_one_or_none()
            if user:
                user.is_banned = True
                user.ban_until = ban_until if data.action_taken == "temp_ban" else None

        await self.db.commit()
        await self.db.refresh(violation)
        return violation

    async def get_user_violations(
        self, user_id: int, skip: int = 0, limit: int = 50
    ) -> list[UserViolation]:
        """获取用户违规记录"""
        result = await self.db.execute(
            select(UserViolation)
            .where(UserViolation.user_id == user_id)
            .order_by(UserViolation.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def check_user_ban_status(self, user_id: int) -> dict:
        """检查用户封禁状态"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            return {"is_banned": False}

        # 检查临时封禁是否过期
        if user.is_banned and user.ban_until:
            if datetime.utcnow() > user.ban_until:
                user.is_banned = False
                user.ban_until = None
                await self.db.commit()
                return {"is_banned": False}

        return {
            "is_banned": user.is_banned,
            "ban_until": user.ban_until,
            "is_permanent": user.is_banned and user.ban_until is None,
        }

    # ============ 内容检查 ============
    async def check_text_content(self, text: str) -> dict:
        """检查文本内容"""
        return await check_content(text, self.db)

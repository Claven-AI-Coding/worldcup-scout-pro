from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Player, PointRecord, Team, User, Wallpaper
from app.schemas.wallpaper import WallpaperCreate, WallpaperResponse
from app.utils.auth import get_current_user

DAILY_WALLPAPER_LIMIT = 5

# 固定模板壁纸（无需 AI 生成）
TEMPLATE_WALLPAPERS = [
    {
        "id": "tpl_1",
        "name": "世界杯 2026 主视觉",
        "style": "official",
        "preview_url": "/static/templates/wc2026_main.jpg",
        "points_cost": 0,
    },
    {
        "id": "tpl_2",
        "name": "赛程日历壁纸",
        "style": "calendar",
        "preview_url": "/static/templates/wc2026_calendar.jpg",
        "points_cost": 0,
    },
    {
        "id": "tpl_3",
        "name": "球队配色壁纸",
        "style": "team_color",
        "preview_url": "/static/templates/wc2026_team_color.jpg",
        "points_cost": 50,
    },
    {
        "id": "tpl_4",
        "name": "复古风格海报",
        "style": "retro",
        "preview_url": "/static/templates/wc2026_retro.jpg",
        "points_cost": 50,
    },
]

# 积分消耗：普通 50 分，高清 100 分，会员免费
DOWNLOAD_COST_NORMAL = 50
DOWNLOAD_COST_HD = 100

router = APIRouter()


def _build_prompt(style: str, team: Team | None, player: Player | None) -> str:
    """Build an AI generation prompt from the given style and subject."""
    subject = "World Cup 2026"
    if team and player:
        subject = f"{player.name} ({player.name_en or ''}) from {team.name} ({team.name_en or ''})"
    elif team:
        subject = f"{team.name} ({team.name_en or ''}) national football team"
    elif player:
        subject = f"football player {player.name} ({player.name_en or ''})"

    style_prompts = {
        "cyberpunk": f"Cyberpunk style digital art of {subject}, neon lights, futuristic stadium, high detail, 4K",
        "ink": f"Traditional Chinese ink painting style of {subject}, elegant brushstrokes, minimalist, artistic",
        "comic": f"Comic book style illustration of {subject}, bold lines, vibrant colors, dynamic pose, action scene",
        "minimal": f"Minimalist modern design of {subject}, clean lines, geometric shapes, team colors, wallpaper",
    }
    return style_prompts.get(style, f"{style} style art of {subject}, high quality, 4K wallpaper")


@router.post("/generate", response_model=WallpaperResponse, status_code=status.HTTP_201_CREATED)
async def generate_wallpaper(
    payload: WallpaperCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a wallpaper (authenticated, daily limit enforced).

    Creates a wallpaper record with status='pending'. The actual image
    generation is handled asynchronously by a background task (Celery).
    """
    # Check daily limit
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    count_stmt = select(func.count()).where(
        Wallpaper.user_id == current_user.id,
        Wallpaper.created_at >= today_start,
    )
    count_result = await db.execute(count_stmt)
    today_count = count_result.scalar_one()

    if today_count >= DAILY_WALLPAPER_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"每日生成上限为 {DAILY_WALLPAPER_LIMIT} 张，今日已用完",
        )

    # Validate team_id if provided
    team: Team | None = None
    if payload.team_id:
        team_result = await db.execute(select(Team).where(Team.id == payload.team_id))
        team = team_result.scalar_one_or_none()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="球队不存在",
            )

    # Validate player_id if provided
    player: Player | None = None
    if payload.player_id:
        player_result = await db.execute(select(Player).where(Player.id == payload.player_id))
        player = player_result.scalar_one_or_none()
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="球员不存在",
            )

    # Build prompt
    prompt = _build_prompt(payload.style, team, player)

    wallpaper = Wallpaper(
        user_id=current_user.id,
        team_id=payload.team_id,
        player_id=payload.player_id,
        style=payload.style,
        prompt=prompt,
        status="pending",
    )
    db.add(wallpaper)
    await db.flush()
    await db.refresh(wallpaper)

    # TODO: dispatch Celery task to generate the wallpaper image
    # from app.tasks.wallpaper import generate_wallpaper_task
    # generate_wallpaper_task.delay(wallpaper.id, prompt)

    return wallpaper


@router.get("/my", response_model=list[WallpaperResponse])
async def get_my_wallpapers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's wallpapers (authenticated)."""
    stmt = (
        select(Wallpaper)
        .where(Wallpaper.user_id == current_user.id)
        .order_by(Wallpaper.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    wallpapers = result.scalars().all()
    return wallpapers


@router.get("/templates")
async def get_template_wallpapers():
    """获取固定模板壁纸列表（无需 AI 生成，即时可用）"""
    return TEMPLATE_WALLPAPERS


@router.post("/{wallpaper_id}/download")
async def download_wallpaper(
    wallpaper_id: int,
    hd: bool = Query(False, description="是否高清版本"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """下载壁纸（消耗积分，会员免费）"""
    # 验证壁纸存在
    wp_result = await db.execute(select(Wallpaper).where(Wallpaper.id == wallpaper_id))
    wallpaper = wp_result.scalar_one_or_none()
    if not wallpaper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="壁纸不存在")

    # 会员免费
    if current_user.is_member:
        return {"message": "会员免费下载", "image_url": wallpaper.image_url}

    # 计算消耗积分
    cost = DOWNLOAD_COST_HD if hd else DOWNLOAD_COST_NORMAL
    if current_user.points < cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"积分不足，需要 {cost} 分，当前 {current_user.points} 分",
        )

    # 扣除积分
    current_user.points -= cost
    record = PointRecord(
        user_id=current_user.id,
        amount=-cost,
        reason="exchange",
        detail=f"下载壁纸 #{wallpaper_id}" + (" (高清)" if hd else ""),
    )
    db.add(record)
    await db.flush()

    return {"message": f"下载成功，消耗 {cost} 积分", "image_url": wallpaper.image_url}


@router.get("/gallery", response_model=list[WallpaperResponse])
async def get_wallpaper_gallery(
    style: str | None = Query(None, description="Filter by style: cyberpunk, ink, comic, minimal"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Public wallpaper gallery showing completed wallpapers, paginated."""
    stmt = select(Wallpaper).where(Wallpaper.status == "done").order_by(Wallpaper.created_at.desc())

    if style:
        stmt = stmt.where(Wallpaper.style == style)

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    wallpapers = result.scalars().all()
    return wallpapers

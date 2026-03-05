from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Comment, Post, Team, User
from app.schemas.post import (
    CommentCreate,
    CommentResponse,
    PostCreate,
    PostListResponse,
    PostResponse,
)
from app.utils.auth import get_current_user
from app.utils.content_filter import check_content

router = APIRouter()


@router.get("/hot", response_model=PostListResponse)
async def list_hot_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """全站热门帖子，按热度算法排序（点赞*3 + 评论*5 + 时间衰减）"""
    from sqlalchemy import case, cast, Float
    from datetime import datetime, timedelta

    # 热度 = likes*3 + comments_count*5，24小时内发布的帖子额外加权
    now = datetime.utcnow()
    recent_cutoff = now - timedelta(hours=24)

    hot_score = (
        Post.likes * 3 + Post.comments_count * 5
        + case((Post.created_at > recent_cutoff, 10), else_=0)
    )

    stmt = (
        select(Post)
        .options(selectinload(Post.author))
        .order_by(hot_score.desc(), Post.created_at.desc())
    )

    count_stmt = select(func.count()).select_from(Post)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    posts = result.scalars().all()

    return PostListResponse(items=posts, total=total)


@router.get("/{team_id}/posts", response_model=PostListResponse)
async def list_team_posts(
    team_id: int,
    sort: str = Query("latest", description="排序方式: latest(最新), hot(热门)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List posts for a team circle, paginated with skip/limit."""
    # Verify team exists
    team_result = await db.execute(select(Team).where(Team.id == team_id))
    if not team_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="球队不存在",
        )

    stmt = (
        select(Post)
        .options(selectinload(Post.author))
        .where(Post.team_id == team_id)
    )
    if sort == "hot":
        stmt = stmt.order_by((Post.likes * 3 + Post.comments_count * 5).desc(), Post.created_at.desc())
    else:
        stmt = stmt.order_by(Post.created_at.desc())

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    posts = result.scalars().all()

    return PostListResponse(items=posts, total=total)


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new post in a team circle (authenticated)."""
    # 内容过滤
    content_check = await check_content(payload.content, db)
    if not content_check["is_clean"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"内容包含违规词汇，请修改后重试",
        )

    # Verify team exists
    team_result = await db.execute(select(Team).where(Team.id == payload.team_id))
    if not team_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="球队不存在",
        )

    post = Post(
        user_id=current_user.id,
        team_id=payload.team_id,
        content=payload.content,
        images=payload.images,
    )
    db.add(post)
    await db.flush()
    await db.refresh(post)

    # Eager-load author for response
    stmt = select(Post).options(selectinload(Post.author)).where(Post.id == post.id)
    result = await db.execute(stmt)
    post = result.scalar_one()

    return post


@router.post("/posts/{post_id}/like", response_model=PostResponse)
async def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Like a post (authenticated). Increments the like counter."""
    result = await db.execute(
        select(Post).options(selectinload(Post.author)).where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在",
        )

    post.likes += 1
    await db.flush()
    await db.refresh(post)
    return post


@router.post("/posts/{post_id}/comment", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    payload: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Comment on a post (authenticated)."""
    # 评论内容过滤
    content_check = await check_content(payload.content, db)
    if not content_check["is_clean"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="评论包含违规词汇，请修改后重试",
        )

    # Verify post exists
    post_result = await db.execute(select(Post).where(Post.id == post_id))
    post = post_result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在",
        )

    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=payload.content,
    )
    db.add(comment)

    # Increment comments count on the post
    post.comments_count += 1

    await db.flush()
    await db.refresh(comment)

    # Eager-load author for response
    stmt = select(Comment).options(selectinload(Comment.author)).where(Comment.id == comment.id)
    result = await db.execute(stmt)
    comment = result.scalar_one()

    return comment


@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
async def list_comments(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """List comments for a post, ordered by creation time."""
    # Verify post exists
    post_result = await db.execute(select(Post).where(Post.id == post_id))
    if not post_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在",
        )

    stmt = (
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    comments = result.scalars().all()
    return comments

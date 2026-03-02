from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostAuthorInfo(BaseModel):
    """Nested author info embedded in post/comment responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nickname: str
    avatar: str | None = None


class PostCreate(BaseModel):
    team_id: int
    content: str = Field(..., min_length=1, max_length=5000)
    images: list[str] | None = None


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    team_id: int
    content: str
    images: list[str] | None = None
    likes: int = 0
    comments_count: int = 0
    created_at: datetime

    author: PostAuthorInfo | None = None


class PostListResponse(BaseModel):
    items: list[PostResponse]
    total: int


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime

    author: PostAuthorInfo | None = None

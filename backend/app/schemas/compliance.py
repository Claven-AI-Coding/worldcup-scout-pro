"""合规管理相关 Pydantic Schema"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ============ 违禁词 ============
class BannedWordCreate(BaseModel):
    word: str = Field(..., min_length=1, max_length=100)
    category: str | None = Field(None, max_length=50)


class BannedWordBatchCreate(BaseModel):
    words: list[str] = Field(..., min_items=1, max_items=1000)
    category: str | None = None


class BannedWordResponse(BaseModel):
    id: int
    word: str
    category: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ 举报 ============
class ReportCreate(BaseModel):
    target_type: str = Field(..., pattern="^(post|comment|user)$")
    target_id: int = Field(..., gt=0)
    reason: str | None = Field(None, max_length=200)


class ReportResponse(BaseModel):
    id: int
    reporter_id: int
    target_type: str
    target_id: int
    reason: str | None
    status: str
    reviewed_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReportReview(BaseModel):
    status: str = Field(..., pattern="^(reviewed|dismissed)$")
    action: str | None = Field(None, pattern="^(none|delete_content|warn_user|ban_user)$")
    ban_days: int | None = Field(None, ge=1, le=365)
    notes: str | None = Field(None, max_length=500)


# ============ 用户违规 ============
class UserViolationCreate(BaseModel):
    user_id: int
    violation_type: str = Field(..., pattern="^(spam|profanity|harassment|illegal)$")
    severity: str = Field("warning", pattern="^(warning|serious|severe)$")
    content: str | None = None
    action_taken: str | None = Field(None, pattern="^(warned|temp_ban|permanent_ban)$")
    ban_days: int | None = Field(None, ge=1, le=365)
    notes: str | None = None


class UserViolationResponse(BaseModel):
    id: int
    user_id: int
    violation_type: str
    severity: str
    content: str | None
    action_taken: str | None
    ban_until: datetime | None
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============ 内容检查 ============
class ContentCheckRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)


class ContentCheckResponse(BaseModel):
    is_clean: bool
    matched_words: list[str]
    categories: list[str]
    filtered_text: str | None = None

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReportCreate(BaseModel):
    target_type: str = Field(..., description="post/comment/user")
    target_id: int
    reason: str | None = Field(None, max_length=200)


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reporter_id: int
    target_type: str
    target_id: int
    reason: str | None = None
    status: str = "pending"
    reviewed_at: datetime | None = None
    created_at: datetime


class ReportListResponse(BaseModel):
    items: list[ReportResponse]
    total: int

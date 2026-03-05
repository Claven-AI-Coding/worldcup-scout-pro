from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PointRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    amount: int
    reason: str
    detail: str | None = None
    created_at: datetime


class PointRecordListResponse(BaseModel):
    items: list[PointRecordResponse]
    total: int

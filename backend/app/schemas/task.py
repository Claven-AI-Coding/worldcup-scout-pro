from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    task_type: str
    completed: bool = False
    points_reward: int
    completed_at: datetime | None = None
    date: date
    created_at: datetime


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int


class SignInResponse(BaseModel):
    points_earned: int
    consecutive_days: int
    total_points: int

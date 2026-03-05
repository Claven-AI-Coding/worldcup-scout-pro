from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)
    agreed_terms: bool = Field(default=False, description="是否同意用户协议和隐私政策")


class UserLogin(BaseModel):
    username: str
    password: str


class WxLoginRequest(BaseModel):
    code: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nickname: str
    avatar: str | None = None
    points: int = 1000
    fav_team_id: int | None = None
    win_streak: int = 0
    title: str | None = None
    phone: str | None = None
    is_member: bool = False
    member_expire_at: datetime | None = None
    member_type: str | None = None
    daily_sign_in: date | None = None
    badges: list | None = None
    agreed_terms: bool = False
    created_at: datetime


class UserUpdateRequest(BaseModel):
    nickname: str | None = Field(None, min_length=1, max_length=64)
    avatar: str | None = None
    phone: str | None = Field(None, max_length=20)
    fav_team_id: int | None = None

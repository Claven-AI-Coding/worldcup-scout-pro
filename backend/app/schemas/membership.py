"""Membership Schema"""

from datetime import datetime

from pydantic import BaseModel, Field


class MembershipPlan(BaseModel):
    """Membership plan"""

    plan_id: str = Field(..., description="monthly/quarterly/yearly")
    name: str
    price: float = Field(..., gt=0)
    duration_days: int = Field(..., gt=0)
    features: list[str]


class SubscribeRequest(BaseModel):
    """Subscribe request"""

    plan_id: str = Field(..., pattern="^(monthly|quarterly|yearly)$")
    payment_method: str = Field(
        ..., pattern="^(wechat|alipay|stripe)$", description="Payment method"
    )


class SubscribeResponse(BaseModel):
    """Subscribe response"""

    order_id: str
    plan_id: str
    amount: float
    payment_url: str | None = None
    qr_code: str | None = None
    expires_at: datetime


class MembershipStatus(BaseModel):
    """Membership status"""

    is_member: bool
    member_type: str | None = None
    expire_at: datetime | None = None
    days_remaining: int | None = None
    features: list[str] = Field(default_factory=list)


class MembershipFeature(BaseModel):
    """Membership feature check"""

    feature_key: str
    is_available: bool
    reason: str | None = None

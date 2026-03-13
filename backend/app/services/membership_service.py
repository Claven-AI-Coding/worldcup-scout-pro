"""Membership Service"""

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.membership import (
    MembershipFeature,
    MembershipPlan,
    MembershipStatus,
    SubscribeRequest,
    SubscribeResponse,
)

# Membership plans configuration
MEMBERSHIP_PLANS = {
    "monthly": MembershipPlan(
        plan_id="monthly",
        name="Monthly Membership",
        price=29.9,
        duration_days=30,
        features=[
            "unlimited_predictions",
            "ai_analysis",
            "advanced_charts",
            "no_ads",
            "priority_support",
        ],
    ),
    "quarterly": MembershipPlan(
        plan_id="quarterly",
        name="Quarterly Membership",
        price=79.9,
        duration_days=90,
        features=[
            "unlimited_predictions",
            "ai_analysis",
            "advanced_charts",
            "no_ads",
            "priority_support",
            "exclusive_badge",
        ],
    ),
    "yearly": MembershipPlan(
        plan_id="yearly",
        name="Yearly Membership",
        price=299.9,
        duration_days=365,
        features=[
            "unlimited_predictions",
            "ai_analysis",
            "advanced_charts",
            "no_ads",
            "priority_support",
            "exclusive_badge",
            "early_access",
            "custom_avatar",
        ],
    ),
}

# Feature access control
MEMBER_FEATURES = {
    "unlimited_predictions": "Unlimited match predictions",
    "ai_analysis": "AI-powered analysis",
    "advanced_charts": "Advanced data visualization",
    "no_ads": "Ad-free experience",
    "priority_support": "Priority customer support",
    "exclusive_badge": "Exclusive member badge",
    "early_access": "Early access to new features",
    "custom_avatar": "Custom avatar frames",
}


class MembershipService:
    """Membership management service"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_plans(self) -> list[MembershipPlan]:
        """Get all membership plans"""
        return list(MEMBERSHIP_PLANS.values())

    async def subscribe(
        self, user_id: int, request: SubscribeRequest
    ) -> SubscribeResponse:
        """Create subscription order"""
        plan = MEMBERSHIP_PLANS.get(request.plan_id)
        if not plan:
            raise ValueError(f"Invalid plan: {request.plan_id}")

        # Generate order ID
        order_id = f"ORD{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{secrets.token_hex(4).upper()}"

        # In production, integrate with payment gateway (WeChat Pay, Alipay, Stripe)
        # For now, return mock payment info
        payment_url = None
        qr_code = None

        if request.payment_method == "wechat":
            payment_url = f"weixin://wxpay/bizpayurl?pr={order_id}"
            qr_code = f"https://api.qrserver.com/v1/create-qr-code/?data={payment_url}"
        elif request.payment_method == "alipay":
            payment_url = f"alipays://platformapi/startapp?appId=20000067&url={order_id}"
            qr_code = f"https://api.qrserver.com/v1/create-qr-code/?data={payment_url}"
        elif request.payment_method == "stripe":
            payment_url = f"https://checkout.stripe.com/pay/{order_id}"

        return SubscribeResponse(
            order_id=order_id,
            plan_id=plan.plan_id,
            amount=plan.price,
            payment_url=payment_url,
            qr_code=qr_code,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        )

    async def activate_membership(
        self, user_id: int, plan_id: str
    ) -> MembershipStatus:
        """Activate membership (called after payment success)"""
        plan = MEMBERSHIP_PLANS.get(plan_id)
        if not plan:
            raise ValueError(f"Invalid plan: {plan_id}")

        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Update user membership
        user.is_member = True
        user.member_type = plan_id
        user.member_expire_at = datetime.now(timezone.utc) + timedelta(
            days=plan.duration_days
        )

        await self.db.commit()
        await self.db.refresh(user)

        return await self.get_status(user_id)

    async def get_status(self, user_id: int) -> MembershipStatus:
        """Get membership status"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Check if membership expired
        if user.is_member and user.member_expire_at:
            if datetime.now(timezone.utc) > user.member_expire_at:
                user.is_member = False
                user.member_type = None
                await self.db.commit()

        days_remaining = None
        features = []

        if user.is_member and user.member_expire_at:
            delta = user.member_expire_at - datetime.now(timezone.utc)
            days_remaining = max(0, delta.days)

            # Get features for current plan
            plan = MEMBERSHIP_PLANS.get(user.member_type or "")
            if plan:
                features = plan.features

        return MembershipStatus(
            is_member=user.is_member,
            member_type=user.member_type,
            expire_at=user.member_expire_at,
            days_remaining=days_remaining,
            features=features,
        )

    async def check_feature(
        self, user_id: int, feature_key: str
    ) -> MembershipFeature:
        """Check if user has access to a feature"""
        status = await self.get_status(user_id)

        is_available = feature_key in status.features
        reason = None

        if not is_available:
            if not status.is_member:
                reason = "Membership required"
            else:
                reason = f"Feature not included in {status.member_type} plan"

        return MembershipFeature(
            feature_key=feature_key, is_available=is_available, reason=reason
        )

    async def cancel_membership(self, user_id: int) -> MembershipStatus:
        """Cancel membership (will expire at the end of current period)"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError(f"User {user_id} not found")

        # In production, cancel auto-renewal in payment gateway
        # For now, just mark as cancelled (membership will expire naturally)

        return await self.get_status(user_id)

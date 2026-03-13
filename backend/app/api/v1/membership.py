"""Membership API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.membership import (
    MembershipFeature,
    MembershipPlan,
    MembershipStatus,
    SubscribeRequest,
    SubscribeResponse,
)
from app.services.membership_service import MembershipService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/membership", tags=["membership"])


@router.get("/plans", response_model=list[MembershipPlan])
async def get_plans(db: AsyncSession = Depends(get_db)):
    """Get all membership plans"""
    service = MembershipService(db)
    return await service.get_plans()


@router.post("/subscribe", response_model=SubscribeResponse)
async def subscribe(
    request: SubscribeRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create subscription order"""
    service = MembershipService(db)
    try:
        return await service.subscribe(current_user.id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/activate/{plan_id}", response_model=MembershipStatus)
async def activate_membership(
    plan_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Activate membership (called after payment success)"""
    service = MembershipService(db)
    try:
        return await service.activate_membership(current_user.id, plan_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status", response_model=MembershipStatus)
async def get_status(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Get current membership status"""
    service = MembershipService(db)
    try:
        return await service.get_status(current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/check-feature/{feature_key}", response_model=MembershipFeature)
async def check_feature(
    feature_key: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Check if user has access to a feature"""
    service = MembershipService(db)
    try:
        return await service.check_feature(current_user.id, feature_key)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/cancel", response_model=MembershipStatus)
async def cancel_membership(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Cancel membership"""
    service = MembershipService(db)
    try:
        return await service.cancel_membership(current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

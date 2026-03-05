"""会员权限控制中间件"""

from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status

from app.models import User
from app.utils.auth import get_current_user


async def require_member(current_user: User = Depends(get_current_user)) -> User:
    """要求会员权限的依赖"""
    if not current_user.is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此功能需要会员权限",
        )

    # 检查会员是否过期
    if current_user.member_expire_at and current_user.member_expire_at < datetime.now(timezone.utc):
        current_user.is_member = False
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="会员已过期，请续费",
        )

    return current_user


def is_member_active(user: User) -> bool:
    """检查用户是否为有效会员"""
    if not user.is_member:
        return False
    if user.member_expire_at and user.member_expire_at < datetime.now(timezone.utc):
        return False
    return True

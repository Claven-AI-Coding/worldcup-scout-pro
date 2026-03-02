from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse, WxLoginRequest
from app.utils.auth import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user with username and password, return JWT token."""
    result = await db.execute(select(User).where(User.username == payload.username))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user with username and password."""
    result = await db.execute(select(User).where(User.username == payload.username))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在",
        )

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        nickname=payload.username,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@router.post("/wx-login", response_model=Token)
async def wx_login(payload: WxLoginRequest, db: AsyncSession = Depends(get_db)):
    """WeChat mini-program login (placeholder).

    In production this would:
    1. Exchange the code for openid via WeChat API
    2. Find or create a user by openid
    3. Return a JWT token
    """
    # TODO: call WeChat API to exchange code for session_key + openid
    # wx_url = f"https://api.weixin.qq.com/sns/jscode2session?appid=...&secret=...&js_code={payload.code}&grant_type=authorization_code"
    # async with httpx.AsyncClient() as client:
    #     resp = await client.get(wx_url)
    #     data = resp.json()
    #     openid = data["openid"]

    openid = f"wx_placeholder_{payload.code}"

    result = await db.execute(select(User).where(User.openid == openid))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            openid=openid,
            username=f"wx_{openid[:16]}",
            nickname="微信用户",
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info."""
    return current_user

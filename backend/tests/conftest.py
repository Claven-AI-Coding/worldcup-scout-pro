"""测试配置 — 使用 SQLite 内存数据库进行隔离测试"""

import os

# 必须在导入 app 之前设置环境变量
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_db
from app.main import app
from app.models import (
    BannedWord,
    Match,
    Team,
    User,
)
from app.utils.auth import create_access_token, hash_password
from app.utils.content_filter import reset_cache

# SQLite 内存数据库测试引擎
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def _patch_jsonb():
    """将 PostgreSQL JSONB 在 SQLite 上编译为 JSON"""
    from sqlalchemy.dialects.postgresql import JSONB
    from sqlalchemy.ext.compiler import compiles

    @compiles(JSONB, "sqlite")
    def _compile_jsonb_sqlite(type_, compiler, **kw):
        return "JSON"


@pytest.fixture
async def engine(_patch_jsonb):
    eng = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()


@pytest.fixture
async def db_session(engine):
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(engine):
    """带数据库依赖覆盖的测试客户端"""
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def _override_get_db():
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession):
    """创建测试用户并返回"""
    user = User(
        username="testuser",
        password_hash=hash_password("test123456"),
        nickname="测试用户",
        agreed_terms=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User):
    """已认证用户的请求头"""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def test_teams(db_session: AsyncSession):
    """创建两个测试球队"""
    team_a = Team(name="巴西", name_en="Brazil", code="BRA", group_name="A")
    team_b = Team(name="德国", name_en="Germany", code="GER", group_name="A")
    db_session.add_all([team_a, team_b])
    await db_session.commit()
    await db_session.refresh(team_a)
    await db_session.refresh(team_b)
    return team_a, team_b


@pytest.fixture
async def test_match(db_session: AsyncSession, test_teams):
    """创建测试比赛"""
    from datetime import datetime, timezone

    team_a, team_b = test_teams
    match = Match(
        stage="group",
        group_name="A",
        home_team_id=team_a.id,
        away_team_id=team_b.id,
        status="upcoming",
        start_time=datetime(2026, 6, 12, 18, 0, tzinfo=timezone.utc),
        venue="MetLife Stadium",
    )
    db_session.add(match)
    await db_session.commit()
    await db_session.refresh(match)
    return match


@pytest.fixture
async def finished_match(db_session: AsyncSession, test_teams):
    """创建已结束的测试比赛"""
    from datetime import datetime, timezone

    team_a, team_b = test_teams
    match = Match(
        stage="group",
        group_name="A",
        home_team_id=team_a.id,
        away_team_id=team_b.id,
        home_score=2,
        away_score=1,
        status="finished",
        start_time=datetime(2026, 6, 10, 18, 0, tzinfo=timezone.utc),
        venue="Rose Bowl",
    )
    db_session.add(match)
    await db_session.commit()
    await db_session.refresh(match)
    return match


@pytest.fixture
async def banned_words(db_session: AsyncSession):
    """加载测试违禁词"""
    reset_cache()
    words = [
        BannedWord(word="脏话测试", category="profanity"),
        BannedWord(word="赌博推荐", category="gambling"),
        BannedWord(word="垃圾广告", category="spam"),
    ]
    db_session.add_all(words)
    await db_session.commit()
    return words

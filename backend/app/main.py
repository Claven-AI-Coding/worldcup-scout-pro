from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, community, legal, matches, players, points, predictions, rankings, reports, tasks, teams, wallpapers
from app.api.websocket import router as ws_router
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    yield
    await app.state.redis.close()


app = FastAPI(
    title="世界杯全能助手・球探 Pro",
    description="World Cup Scout Pro API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(matches.router, prefix="/api/v1/matches", tags=["赛程"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["球队"])
app.include_router(players.router, prefix="/api/v1/players", tags=["球员"])
app.include_router(community.router, prefix="/api/v1/community", tags=["社区"])
app.include_router(predictions.router, prefix="/api/v1/predictions", tags=["竞猜"])
app.include_router(wallpapers.router, prefix="/api/v1/wallpapers", tags=["壁纸"])
app.include_router(rankings.router, prefix="/api/v1/rankings", tags=["排行榜"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["任务"])
app.include_router(points.router, prefix="/api/v1/points", tags=["积分"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["举报"])
app.include_router(legal.router, prefix="/api/v1/legal", tags=["法律文本"])
app.include_router(ws_router, prefix="/api/v1/ws", tags=["WebSocket"])


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "worldcup-scout-pro"}

from app.schemas.match import (
    MatchEventResponse,
    MatchListResponse,
    MatchResponse,
    MatchTeamInfo,
    ReminderCreate,
    ReminderResponse,
)
from app.schemas.player import PlayerListResponse, PlayerResponse
from app.schemas.post import (
    CommentCreate,
    CommentResponse,
    PostAuthorInfo,
    PostCreate,
    PostListResponse,
    PostResponse,
)
from app.schemas.prediction import LeaderboardEntry, PredictionCreate, PredictionResponse
from app.schemas.team import TeamListResponse, TeamResponse
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse, WxLoginRequest
from app.schemas.wallpaper import WallpaperCreate, WallpaperResponse

__all__ = [
    # User
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "WxLoginRequest",
    # Team
    "TeamResponse",
    "TeamListResponse",
    # Player
    "PlayerResponse",
    "PlayerListResponse",
    # Match
    "MatchTeamInfo",
    "MatchResponse",
    "MatchEventResponse",
    "MatchListResponse",
    "ReminderCreate",
    "ReminderResponse",
    # Post
    "PostAuthorInfo",
    "PostCreate",
    "PostResponse",
    "PostListResponse",
    "CommentCreate",
    "CommentResponse",
    # Prediction
    "PredictionCreate",
    "PredictionResponse",
    "LeaderboardEntry",
    # Wallpaper
    "WallpaperCreate",
    "WallpaperResponse",
]

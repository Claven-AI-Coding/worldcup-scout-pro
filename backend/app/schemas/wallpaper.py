from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WallpaperCreate(BaseModel):
    team_id: int | None = None
    player_id: int | None = None
    style: str = Field(..., pattern=r"^(cyberpunk|ink|comic|minimal)$")


class WallpaperResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    team_id: int | None = None
    player_id: int | None = None
    style: str
    prompt: str
    image_url: str | None = None
    status: str = "pending"
    created_at: datetime

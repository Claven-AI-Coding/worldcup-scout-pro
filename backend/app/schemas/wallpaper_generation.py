"""Wallpaper Generation Schema"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class WallpaperStyle(str, Enum):
    """Wallpaper style"""

    CYBERPUNK = "cyberpunk"
    WATERCOLOR = "watercolor"
    COMIC = "comic"
    MINIMALIST = "minimalist"
    REALISTIC = "realistic"


class WallpaperGenerateRequest(BaseModel):
    """Wallpaper generation request"""

    team_id: int = Field(..., gt=0)
    style: WallpaperStyle
    custom_text: str | None = Field(None, max_length=100)


class WallpaperResponse(BaseModel):
    """Wallpaper response"""

    id: int
    team_id: int
    team_name: str
    style: str
    image_url: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)

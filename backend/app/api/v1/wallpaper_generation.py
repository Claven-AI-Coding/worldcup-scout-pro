"""Wallpaper Generation API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.wallpaper_generation import (
    WallpaperGenerateRequest,
    WallpaperResponse,
)
from app.services.wallpaper_generation_service import WallpaperGenerationService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/wallpapers", tags=["wallpapers"])


@router.post("/generate", response_model=WallpaperResponse)
async def generate_wallpaper(
    request: WallpaperGenerateRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate AI wallpaper"""
    service = WallpaperGenerationService(db)
    try:
        return await service.generate_wallpaper(current_user.id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/my-wallpapers", response_model=list[WallpaperResponse])
async def get_my_wallpapers(
    skip: int = 0,
    limit: int = 20,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's generated wallpapers"""
    service = WallpaperGenerationService(db)
    return await service.get_user_wallpapers(current_user.id, skip, limit)


@router.post("/toggle-favorite/{wallpaper_id}")
async def toggle_favorite(
    wallpaper_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Toggle wallpaper favorite status"""
    service = WallpaperGenerationService(db)
    try:
        is_favorite = await service.toggle_favorite(current_user.id, wallpaper_id)
        return {"is_favorite": is_favorite}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

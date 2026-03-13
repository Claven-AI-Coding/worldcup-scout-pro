"""Wallpaper Generation Service"""

import base64
import io
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.team import Team
from app.models.wallpaper import Wallpaper
from app.schemas.wallpaper_generation import (
    WallpaperGenerateRequest,
    WallpaperResponse,
    WallpaperStyle,
)


class WallpaperGenerationService:
    """Wallpaper generation service using AI"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_wallpaper(
        self, user_id: int, request: WallpaperGenerateRequest
    ) -> WallpaperResponse:
        """Generate wallpaper using AI"""
        # Get team info
        team_result = await self.db.execute(
            select(Team).where(Team.id == request.team_id)
        )
        team = team_result.scalar_one_or_none()
        if not team:
            raise ValueError(f"Team {request.team_id} not found")

        # Build prompt based on style
        prompt = self._build_prompt(team, request.style, request.custom_text)

        # Call AI image generation API
        image_url = await self._generate_image(prompt)

        # Save to database
        wallpaper = Wallpaper(
            user_id=user_id,
            team_id=request.team_id,
            style=request.style.value,
            image_url=image_url,
            prompt=prompt,
            is_favorite=False,
        )
        self.db.add(wallpaper)
        await self.db.commit()
        await self.db.refresh(wallpaper)

        return WallpaperResponse(
            id=wallpaper.id,
            team_id=wallpaper.team_id,
            team_name=team.name,
            style=wallpaper.style,
            image_url=wallpaper.image_url,
            created_at=wallpaper.created_at.isoformat(),
        )

    def _build_prompt(
        self, team: Team, style: WallpaperStyle, custom_text: str | None
    ) -> str:
        """Build image generation prompt"""
        team_name = team.name
        team_colors = self._get_team_colors(team.name_en)

        style_descriptions = {
            WallpaperStyle.CYBERPUNK: "cyberpunk style, neon colors, futuristic, high-tech",
            WallpaperStyle.WATERCOLOR: "watercolor painting style, artistic, soft colors",
            WallpaperStyle.COMIC: "comic book style, bold lines, vibrant colors",
            WallpaperStyle.MINIMALIST: "minimalist design, clean lines, simple shapes",
            WallpaperStyle.REALISTIC: "photorealistic, professional photography, stadium background",
        }

        style_desc = style_descriptions.get(style, "modern design")

        prompt = f"""Create a stunning {style_desc} wallpaper for {team_name} football team.
        
Team colors: {team_colors}
Include: Team logo, players in action, stadium atmosphere
Resolution: 1080x1920 (mobile wallpaper)
Quality: 4K, professional, vibrant
"""

        if custom_text:
            prompt += f"Add text: {custom_text}\n"

        prompt += "Make it inspiring and energetic for football fans."

        return prompt

    async def _generate_image(self, prompt: str) -> str:
        """Generate image using AI API"""
        # In production, integrate with:
        # - Stable Diffusion API
        # - DALL-E API
        # - Midjourney API
        # For now, return mock URL

        # Mock implementation - in production, call actual API
        try:
            # Example: Call Stable Diffusion API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.SD_API_URL}/api/v1/txt2img",
                    json={
                        "prompt": prompt,
                        "negative_prompt": "blurry, low quality, distorted",
                        "steps": 20,
                        "cfg_scale": 7.5,
                        "width": 1080,
                        "height": 1920,
                        "sampler_name": "DPM++ 2M Karras",
                    },
                    timeout=60.0,
                )

                if response.status_code == 200:
                    data = response.json()
                    # Return first image URL
                    if data.get("images"):
                        return data["images"][0]
        except Exception:
            pass

        # Fallback: return placeholder
        return f"https://via.placeholder.com/1080x1920?text=Wallpaper"

    def _get_team_colors(self, team_code: str) -> str:
        """Get team colors"""
        team_colors = {
            "ARG": "light blue and white",
            "BRA": "yellow and green",
            "FRA": "blue, white and red",
            "GER": "black, red and gold",
            "ESP": "red and yellow",
            "ENG": "white and red",
            "ITA": "blue, white and green",
            "NED": "orange",
            "POR": "red and green",
            "USA": "blue, white and red",
            "MEX": "green, white and red",
            "ARG": "light blue and white",
        }
        return team_colors.get(team_code, "team colors")

    async def get_user_wallpapers(
        self, user_id: int, skip: int = 0, limit: int = 20
    ) -> list[WallpaperResponse]:
        """Get user's generated wallpapers"""
        result = await self.db.execute(
            select(Wallpaper)
            .where(Wallpaper.user_id == user_id)
            .order_by(Wallpaper.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        wallpapers = result.scalars().all()

        responses = []
        for wp in wallpapers:
            team_result = await self.db.execute(
                select(Team).where(Team.id == wp.team_id)
            )
            team = team_result.scalar_one_or_none()

            responses.append(
                WallpaperResponse(
                    id=wp.id,
                    team_id=wp.team_id,
                    team_name=team.name if team else "Unknown",
                    style=wp.style,
                    image_url=wp.image_url,
                    created_at=wp.created_at.isoformat(),
                )
            )

        return responses

    async def toggle_favorite(self, user_id: int, wallpaper_id: int) -> bool:
        """Toggle wallpaper favorite status"""
        result = await self.db.execute(
            select(Wallpaper).where(
                Wallpaper.id == wallpaper_id, Wallpaper.user_id == user_id
            )
        )
        wallpaper = result.scalar_one_or_none()
        if not wallpaper:
            raise ValueError("Wallpaper not found")

        wallpaper.is_favorite = not wallpaper.is_favorite
        await self.db.commit()
        await self.db.refresh(wallpaper)

        return wallpaper.is_favorite

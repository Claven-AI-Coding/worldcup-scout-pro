"""Celery task for asynchronous wallpaper generation."""

import asyncio
import logging

from app.database import async_session
from app.models.wallpaper import Wallpaper
from app.services.wallpaper import generate_wallpaper_image, generate_wallpaper_prompt
from app.tasks import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Run an async coroutine in a new event loop (for use inside sync Celery tasks)."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="tasks.generate_wallpaper", bind=True, max_retries=2)
def generate_wallpaper_task(
    self,
    wallpaper_id: int,
    team_name: str,
    player_name: str | None = None,
    style: str = "cyberpunk",
):
    """Generate a wallpaper image asynchronously and update the database record.

    Args:
        wallpaper_id: ID of the ``Wallpaper`` record to update.
        team_name: National team name.
        player_name: Optional player name.
        style: Wallpaper style (cyberpunk, ink, comic, minimal).
    """
    try:

        async def _generate():
            async with async_session() as db:
                # Load the wallpaper record.
                wallpaper = await db.get(Wallpaper, wallpaper_id)
                if wallpaper is None:
                    logger.error("Wallpaper record %d not found", wallpaper_id)
                    return None

                wallpaper.status = "generating"
                await db.flush()

                # Build prompt and generate image.
                prompt = generate_wallpaper_prompt(team_name, player_name, style)
                wallpaper.prompt = prompt

                result = await generate_wallpaper_image(prompt, style)

                wallpaper.image_url = result["url"]
                wallpaper.status = "done"
                await db.commit()

                logger.info("Wallpaper %d generated successfully", wallpaper_id)
                return {
                    "wallpaper_id": wallpaper_id,
                    "image_url": result["url"],
                    "status": "done",
                }

        return _run_async(_generate())

    except Exception as exc:
        logger.exception("Failed to generate wallpaper %d", wallpaper_id)

        # Mark as failed in the database.
        try:

            async def _mark_failed():
                async with async_session() as db:
                    wallpaper = await db.get(Wallpaper, wallpaper_id)
                    if wallpaper:
                        wallpaper.status = "failed"
                        await db.commit()

            _run_async(_mark_failed())
        except Exception:
            logger.exception("Failed to mark wallpaper %d as failed", wallpaper_id)

        raise self.retry(exc=exc, countdown=120)

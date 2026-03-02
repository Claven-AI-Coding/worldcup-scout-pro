"""Celery task for periodically syncing match data from the external API."""

import asyncio
import logging

from app.database import async_session
from app.services.data_sync import sync_live_scores, sync_matches, sync_teams
from app.tasks import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Run an async coroutine in a new event loop (for use inside sync Celery tasks)."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="tasks.sync_all_matches", bind=True, max_retries=3)
def sync_all_matches_task(self):
    """Sync all match data (teams + matches) from Football-Data.org.

    Intended to run every few hours via Celery Beat.
    """
    try:

        async def _sync():
            async with async_session() as db:
                teams_count = await sync_teams(db)
                matches_count = await sync_matches(db)
                await db.commit()
                return {"teams": teams_count, "matches": matches_count}

        result = _run_async(_sync())
        logger.info("Sync all matches completed: %s", result)
        return result

    except Exception as exc:
        logger.exception("Failed to sync matches")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(name="tasks.sync_live_scores", bind=True, max_retries=3)
def sync_live_scores_task(self):
    """Sync live scores for currently ongoing matches.

    Intended to run every 1-2 minutes during match windows.
    """
    try:

        async def _sync():
            async with async_session() as db:
                count = await sync_live_scores(db)
                await db.commit()
                return {"live_updated": count}

        result = _run_async(_sync())
        logger.info("Sync live scores completed: %s", result)
        return result

    except Exception as exc:
        logger.exception("Failed to sync live scores")
        raise self.retry(exc=exc, countdown=30)

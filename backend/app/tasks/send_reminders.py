"""Celery task for checking and sending match reminders."""

import asyncio
import logging

from app.database import async_session
from app.services.reminder import check_and_send_reminders
from app.tasks import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Run an async coroutine in a new event loop (for use inside sync Celery tasks)."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="tasks.check_reminders", bind=True, max_retries=3)
def check_reminders_task(self):
    """Check for due reminders and trigger notifications.

    Intended to run every minute via Celery Beat.
    """
    try:

        async def _check():
            async with async_session() as db:
                triggered = await check_and_send_reminders(db)
                await db.commit()
                return triggered

        triggered = _run_async(_check())

        # In a production system, each triggered reminder would be sent
        # to the user via push notification / WebSocket / WeChat template message.
        for reminder_info in triggered:
            logger.info(
                "Reminder triggered: user=%s match=%s (%s vs %s at %s)",
                reminder_info["username"],
                reminder_info["match_id"],
                reminder_info["home_team"],
                reminder_info["away_team"],
                reminder_info["start_time"],
            )

        return {"triggered": len(triggered), "details": triggered}

    except Exception as exc:
        logger.exception("Failed to check reminders")
        raise self.retry(exc=exc, countdown=30)

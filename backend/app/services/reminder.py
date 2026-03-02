"""Reminder service -- create and check match reminders."""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.match import Match
from app.models.user import Reminder

logger = logging.getLogger(__name__)


async def create_reminder(
    db: AsyncSession,
    user_id: int,
    match_id: int,
    minutes: int = 30,
) -> Reminder:
    """Create a new reminder for a user/match combination.

    If the user already has a reminder for this match, update the reminder
    interval instead of creating a duplicate.

    Args:
        db: Async database session.
        user_id: ID of the user.
        match_id: ID of the match.
        minutes: Minutes before kickoff to send the reminder.

    Returns:
        The created or updated ``Reminder`` instance.
    """
    result = await db.execute(
        select(Reminder).where(
            Reminder.user_id == user_id,
            Reminder.match_id == match_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing is not None:
        existing.remind_before_minutes = minutes
        existing.sent = False
        await db.flush()
        return existing

    reminder = Reminder(
        user_id=user_id,
        match_id=match_id,
        remind_before_minutes=minutes,
    )
    db.add(reminder)
    await db.flush()
    return reminder


async def check_and_send_reminders(db: AsyncSession) -> list[dict]:
    """Find all unsent reminders that are now due and mark them as sent.

    A reminder is *due* when the current time is past
    ``match.start_time - remind_before_minutes``.

    Returns:
        A list of dicts with information about each reminder that was triggered,
        suitable for downstream notification delivery.
    """
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(Reminder)
        .options(
            selectinload(Reminder.match).selectinload(Match.home_team),
            selectinload(Reminder.match).selectinload(Match.away_team),
            selectinload(Reminder.user),
        )
        .where(
            Reminder.sent == False,  # noqa: E712
        )
    )
    reminders = list(result.scalars().all())

    triggered: list[dict] = []
    for reminder in reminders:
        match = reminder.match
        if match is None or match.status == "finished":
            # Match no longer relevant -- mark as sent to skip in future.
            reminder.sent = True
            continue

        remind_at = match.start_time - timedelta(minutes=reminder.remind_before_minutes)
        if now >= remind_at:
            reminder.sent = True
            triggered.append(
                {
                    "reminder_id": reminder.id,
                    "user_id": reminder.user_id,
                    "username": reminder.user.username if reminder.user else None,
                    "match_id": match.id,
                    "home_team": match.home_team.name if match.home_team else "TBD",
                    "away_team": match.away_team.name if match.away_team else "TBD",
                    "start_time": match.start_time.isoformat(),
                    "remind_before_minutes": reminder.remind_before_minutes,
                }
            )

    await db.flush()
    logger.info("Triggered %d reminders", len(triggered))
    return triggered

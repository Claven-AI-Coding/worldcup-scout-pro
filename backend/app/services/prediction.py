"""Prediction settlement service -- settle predictions and update user rankings."""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.match import Match
from app.models.prediction import Prediction
from app.models.user import User

logger = logging.getLogger(__name__)

# Scoring multipliers
EXACT_SCORE_MULTIPLIER = 3.0
CORRECT_RESULT_MULTIPLIER = 1.5

# Win-streak title thresholds
TITLE_THRESHOLDS: list[tuple[int, str]] = [
    (10, "预言帝"),      # 10+ streak
    (7, "神算子"),       # 7-9 streak
    (5, "竞猜达人"),     # 5-6 streak
    (3, "小有所成"),     # 3-4 streak
]


def _determine_result(home_score: int, away_score: int) -> str:
    """Return ``'home'``, ``'draw'``, or ``'away'`` based on the score."""
    if home_score > away_score:
        return "home"
    elif home_score == away_score:
        return "draw"
    else:
        return "away"


def _compute_title(win_streak: int) -> str | None:
    """Determine user title based on consecutive correct predictions."""
    for threshold, title in TITLE_THRESHOLDS:
        if win_streak >= threshold:
            return title
    return None


async def settle_match_predictions(db: AsyncSession, match_id: int) -> int:
    """Settle all unsettled predictions for a finished match.

    Scoring rules:
    - **Exact score**: ``points_wagered * 3``
    - **Correct result** (home/draw/away): ``points_wagered * 1.5``
    - **Wrong**: ``-points_wagered`` (lose the wagered points)

    After settling, the user's ``points``, ``win_streak``, and ``title`` are updated.

    Args:
        db: Async database session.
        match_id: ID of the finished match.

    Returns:
        Number of predictions settled.
    """
    # Load the match.
    match_result = await db.execute(select(Match).where(Match.id == match_id))
    match = match_result.scalar_one_or_none()

    if match is None:
        logger.warning("Match %d not found for settlement", match_id)
        return 0

    if match.status != "finished":
        logger.warning("Match %d is not finished (status=%s), skipping", match_id, match.status)
        return 0

    if match.home_score is None or match.away_score is None:
        logger.warning("Match %d has no final score, skipping", match_id)
        return 0

    actual_result = _determine_result(match.home_score, match.away_score)

    # Fetch unsettled predictions for this match.
    pred_result = await db.execute(
        select(Prediction)
        .options(selectinload(Prediction.user))
        .where(
            Prediction.match_id == match_id,
            Prediction.settled == False,  # noqa: E712
        )
    )
    predictions = list(pred_result.scalars().all())

    settled_count = 0
    for pred in predictions:
        user: User = pred.user
        wagered = pred.points_wagered

        # Check for exact score match.
        exact = (
            pred.predicted_home_score is not None
            and pred.predicted_away_score is not None
            and pred.predicted_home_score == match.home_score
            and pred.predicted_away_score == match.away_score
        )

        correct_result = pred.predicted_result == actual_result

        if exact:
            earned = int(wagered * EXACT_SCORE_MULTIPLIER)
            pred.points_earned = earned
            user.points += earned
            user.win_streak += 1
        elif correct_result:
            earned = int(wagered * CORRECT_RESULT_MULTIPLIER)
            pred.points_earned = earned
            user.points += earned
            user.win_streak += 1
        else:
            pred.points_earned = -wagered
            user.points -= wagered
            user.win_streak = 0

        # Ensure points don't go below zero.
        if user.points < 0:
            user.points = 0

        # Update title based on current win streak.
        user.title = _compute_title(user.win_streak)

        pred.settled = True
        settled_count += 1

    await db.flush()
    logger.info("Settled %d predictions for match %d", settled_count, match_id)
    return settled_count

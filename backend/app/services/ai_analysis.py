"""AI analysis service -- match previews and summaries powered by Claude."""

import logging
from typing import Any

import anthropic

from app.config import settings

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "你是一位资深的足球评论员和数据分析师，专注于世界杯赛事分析。"
    "请用中文回答，语言专业但易于理解，适合广大球迷阅读。"
    "分析应包含数据支撑、战术解读和观赏建议。"
)


async def generate_match_preview(
    home_team: str,
    away_team: str,
    *,
    extra_context: str | None = None,
) -> str:
    """Generate a pre-match analysis using the Claude API.

    Args:
        home_team: Name of the home team.
        away_team: Name of the away team.
        extra_context: Optional additional context (e.g. recent form, injuries).

    Returns:
        Markdown-formatted match preview text.
    """
    user_message = (
        f"请为即将进行的世界杯比赛生成一篇赛前分析：\n\n"
        f"主队: {home_team}\n"
        f"客队: {away_team}\n\n"
        "请包含以下内容：\n"
        "1. 两队历史交锋记录与近期状态\n"
        "2. 关键球员对位分析\n"
        "3. 战术体系与风格特点\n"
        "4. 比赛看点与关键因素\n"
        "5. 比分预测与理由\n"
    )

    if extra_context:
        user_message += f"\n补充信息：\n{extra_context}\n"

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    try:
        message = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )
        content = message.content[0].text
        logger.info(
            "Generated match preview for %s vs %s (%d chars)",
            home_team,
            away_team,
            len(content),
        )
        return content

    except Exception:
        logger.exception("Failed to generate match preview via Claude API")
        raise


async def generate_match_summary(match_data: dict[str, Any]) -> str:
    """Generate a post-match summary using the Claude API.

    Args:
        match_data: Dictionary containing match information with keys:
            - ``home_team``: Home team name.
            - ``away_team``: Away team name.
            - ``home_score``: Final home score.
            - ``away_score``: Final away score.
            - ``events``: List of match events (goals, cards, etc.).
            - ``venue``: (optional) Stadium name.

    Returns:
        Markdown-formatted match summary text.
    """
    home_team = match_data.get("home_team", "未知")
    away_team = match_data.get("away_team", "未知")
    home_score = match_data.get("home_score", 0)
    away_score = match_data.get("away_score", 0)
    events = match_data.get("events", [])
    venue = match_data.get("venue", "")

    events_text = ""
    if events:
        events_lines = []
        for evt in events:
            minute = evt.get("minute", "?")
            event_type = evt.get("event_type", "")
            detail = evt.get("detail", "")
            events_lines.append(f"  - {minute}' [{event_type}] {detail}")
        events_text = "\n".join(events_lines)

    user_message = (
        f"请为以下世界杯比赛生成一篇赛后总结：\n\n"
        f"比赛: {home_team} {home_score} - {away_score} {away_team}\n"
    )
    if venue:
        user_message += f"场地: {venue}\n"
    if events_text:
        user_message += f"\n比赛事件:\n{events_text}\n"

    user_message += (
        "\n请包含以下内容：\n"
        "1. 比赛整体评价\n"
        "2. 关键时刻回顾\n"
        "3. 最佳球员表现\n"
        "4. 战术分析与亮点\n"
        "5. 对后续赛事的影响\n"
    )

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    try:
        message = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )
        content = message.content[0].text
        logger.info(
            "Generated match summary for %s vs %s (%d chars)",
            home_team,
            away_team,
            len(content),
        )
        return content

    except Exception:
        logger.exception("Failed to generate match summary via Claude API")
        raise

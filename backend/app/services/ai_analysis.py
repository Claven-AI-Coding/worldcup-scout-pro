"""AI analysis service -- match previews, summaries, and predictions powered by Claude."""

import json
import logging
from typing import Any

import anthropic

from app.config import settings

logger = logging.getLogger(__name__)

# Redis 缓存键前缀
PREDICTION_CACHE_PREFIX = "match_prediction:"
PREDICTION_CACHE_TTL = 86400  # 24 小时

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


async def generate_match_prediction(
    home_team: str,
    away_team: str,
    *,
    home_stats: dict | None = None,
    away_stats: dict | None = None,
    redis_client=None,
    match_id: int | None = None,
) -> dict[str, Any]:
    """生成 AI 赛果预测（胜率 + 比分区间）

    Returns:
        {
            "home_win_pct": 45.0,
            "draw_pct": 25.0,
            "away_win_pct": 30.0,
            "predicted_scores": [
                {"score": "1-0", "probability": 18.0},
                {"score": "2-1", "probability": 15.0},
                ...
            ],
            "analysis": "简短分析文本",
            "disclaimer": "预测仅供参考，不构成任何投注建议",
        }
    """
    # 检查 Redis 缓存
    cache_key = f"{PREDICTION_CACHE_PREFIX}{match_id}" if match_id else None
    if redis_client and cache_key:
        cached = await redis_client.get(cache_key)
        if cached:
            logger.info("Cache hit for prediction: %s", cache_key)
            return json.loads(cached)

    # 构建 prompt
    context_parts = []
    if home_stats:
        context_parts.append(f"主队数据: FIFA排名#{home_stats.get('fifa_ranking', '?')}, "
                             f"大洲={home_stats.get('confederation', '?')}, "
                             f"历史最佳={home_stats.get('best_result', '?')}")
    if away_stats:
        context_parts.append(f"客队数据: FIFA排名#{away_stats.get('fifa_ranking', '?')}, "
                             f"大洲={away_stats.get('confederation', '?')}, "
                             f"历史最佳={away_stats.get('best_result', '?')}")

    user_message = (
        f"请预测世界杯比赛结果，严格以 JSON 格式返回：\n\n"
        f"主队: {home_team}\n"
        f"客队: {away_team}\n"
    )
    if context_parts:
        user_message += "\n" + "\n".join(context_parts) + "\n"

    user_message += (
        "\n请返回以下 JSON 格式（不要包含 markdown 代码块标记）：\n"
        '{\n'
        '  "home_win_pct": <主胜概率>,\n'
        '  "draw_pct": <平局概率>,\n'
        '  "away_win_pct": <客胜概率>,\n'
        '  "predicted_scores": [\n'
        '    {"score": "<比分>", "probability": <概率>}\n'
        '  ],\n'
        '  "analysis": "<50字以内简短分析>"\n'
        '}\n'
        "注意: 三个概率之和必须等于 100.0，predicted_scores 给出 5 个最可能的比分。"
    )

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    try:
        message = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=512,
            system="你是足球数据分析师，仅返回 JSON 格式数据，不加任何解释。",
            messages=[{"role": "user", "content": user_message}],
        )
        raw = message.content[0].text.strip()
        # 清理可能的 markdown 标记
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        prediction = json.loads(raw.strip())
    except Exception:
        logger.exception("Failed to generate prediction via Claude API, using fallback")
        # 降级为基于 FIFA 排名的简单计算
        home_rank = (home_stats or {}).get("fifa_ranking", 50)
        away_rank = (away_stats or {}).get("fifa_ranking", 50)
        total = home_rank + away_rank
        home_pct = round((1 - home_rank / total) * 80 + 10, 1)
        away_pct = round((1 - away_rank / total) * 80 + 10, 1)
        draw_pct = round(100 - home_pct - away_pct, 1)
        prediction = {
            "home_win_pct": home_pct,
            "draw_pct": max(draw_pct, 5),
            "away_win_pct": away_pct,
            "predicted_scores": [
                {"score": "1-0", "probability": 20.0},
                {"score": "1-1", "probability": 18.0},
                {"score": "2-1", "probability": 15.0},
                {"score": "0-0", "probability": 12.0},
                {"score": "2-0", "probability": 10.0},
            ],
            "analysis": f"基于 FIFA 排名，{home_team}(#{home_rank}) vs {away_team}(#{away_rank})",
        }

    prediction["disclaimer"] = "预测仅供参考，不构成任何投注建议"

    # 写入 Redis 缓存
    if redis_client and cache_key:
        await redis_client.setex(cache_key, PREDICTION_CACHE_TTL, json.dumps(prediction, ensure_ascii=False))
        logger.info("Cached prediction: %s", cache_key)

    return prediction

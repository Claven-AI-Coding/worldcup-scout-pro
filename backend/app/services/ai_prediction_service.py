"""AI 预测服务层"""

import json
from typing import Any

from anthropic import AsyncAnthropic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.match import Match
from app.models.team import Team
from app.schemas.ai_prediction import MatchPredictionResponse, TeamStrengthResponse


class AIPredictionService:
    """AI 预测服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def predict_match(self, match_id: int) -> MatchPredictionResponse:
        """预测比赛结果"""
        # 获取比赛信息
        result = await self.db.execute(select(Match).where(Match.id == match_id))
        match = result.scalar_one_or_none()
        if not match:
            raise ValueError(f"Match {match_id} not found")

        # 获取球队信息
        team1_result = await self.db.execute(select(Team).where(Team.id == match.team1_id))
        team1 = team1_result.scalar_one_or_none()

        team2_result = await self.db.execute(select(Team).where(Team.id == match.team2_id))
        team2 = team2_result.scalar_one_or_none()

        if not team1 or not team2:
            raise ValueError("Teams not found")

        # 构建 AI 提示词
        prompt = self._build_prediction_prompt(match, team1, team2)

        # 调用 Claude API
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        # 解析 AI 响应
        ai_text = response.content[0].text
        prediction_data = self._parse_ai_response(ai_text)

        return MatchPredictionResponse(
            match_id=match_id,
            team1_name=team1.name,
            team2_name=team2.name,
            team1_win_prob=prediction_data["team1_win_prob"],
            draw_prob=prediction_data["draw_prob"],
            team2_win_prob=prediction_data["team2_win_prob"],
            predicted_score=prediction_data["predicted_score"],
            confidence=prediction_data["confidence"],
            key_factors=prediction_data["key_factors"],
            analysis=prediction_data["analysis"],
        )

    def _build_prediction_prompt(self, match: Match, team1: Team, team2: Team) -> str:
        """构建预测提示词"""
        team1_stats = team1.stats or {}
        team2_stats = team2.stats or {}

        prompt = f"""你是一位专业的足球分析师。请分析以下世界杯比赛并给出预测。

比赛信息：
- 主队：{team1.name} ({team1.name_en})
- 客队：{team2.name} ({team2.name_en})
- 阶段：{match.stage}
- 场地：{match.venue or "待定"}

{team1.name} 数据：
- FIFA 排名：{team1_stats.get("fifa_ranking", "N/A")}
- 所属联盟：{team1_stats.get("confederation", "N/A")}
- 世界杯参赛次数：{team1_stats.get("appearances", "N/A")}
- 最好成绩：{team1_stats.get("best_result", "N/A")}
- 教练：{team1.coach}

{team2.name} 数据：
- FIFA 排名：{team2_stats.get("fifa_ranking", "N/A")}
- 所属联盟：{team2_stats.get("confederation", "N/A")}
- 世界杯参赛次数：{team2_stats.get("appearances", "N/A")}
- 最好成绩：{team2_stats.get("best_result", "N/A")}
- 教练：{team2.coach}

请以 JSON 格式返回预测结果：
{{
  "team1_win_prob": 0.45,  // 主队胜率 0-1
  "draw_prob": 0.25,        // 平局概率 0-1
  "team2_win_prob": 0.30,   // 客队胜率 0-1
  "predicted_score": "2-1", // 预测比分
  "confidence": 0.75,       // 预测置信度 0-1
  "key_factors": [          // 关键影响因素（3-5 个）
    "主队 FIFA 排名更高",
    "客队近期状态不佳",
    "主场优势"
  ],
  "analysis": "基于双方实力对比和历史数据，主队具有明显优势..."  // 100-200 字分析
}}

注意：
1. 三个概率之和必须等于 1
2. 分析要客观、专业，基于数据
3. 只返回 JSON，不要其他文字
"""
        return prompt

    def _parse_ai_response(self, ai_text: str) -> dict[str, Any]:
        """解析 AI 响应"""
        try:
            # 尝试提取 JSON
            start = ai_text.find("{")
            end = ai_text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = ai_text[start:end]
                data = json.loads(json_str)

                # 验证概率和
                total_prob = data["team1_win_prob"] + data["draw_prob"] + data["team2_win_prob"]
                if abs(total_prob - 1.0) > 0.01:
                    # 归一化
                    data["team1_win_prob"] /= total_prob
                    data["draw_prob"] /= total_prob
                    data["team2_win_prob"] /= total_prob

                return data
        except Exception:
            pass

        # 解析失败，返回默认值
        return {
            "team1_win_prob": 0.4,
            "draw_prob": 0.3,
            "team2_win_prob": 0.3,
            "predicted_score": "1-1",
            "confidence": 0.5,
            "key_factors": ["数据不足", "需要更多信息"],
            "analysis": "由于数据有限，预测结果仅供参考。",
        }

    async def get_team_strength(self, team_id: int) -> TeamStrengthResponse:
        """获取球队实力评估"""
        result = await self.db.execute(select(Team).where(Team.id == team_id))
        team = result.scalar_one_or_none()
        if not team:
            raise ValueError(f"Team {team_id} not found")

        stats = team.stats or {}
        fifa_ranking = stats.get("fifa_ranking", 50)

        # 基于 FIFA 排名计算评分（简化算法）
        # 排名越低（数字越小）评分越高
        overall_rating = max(0, min(100, 100 - (fifa_ranking - 1) * 0.8))

        # 模拟各项评分（实际应该基于更多数据）
        attack_rating = overall_rating + (hash(team.name) % 20 - 10)
        defense_rating = overall_rating + (hash(team.name + "def") % 20 - 10)
        midfield_rating = overall_rating + (hash(team.name + "mid") % 20 - 10)
        form_rating = overall_rating + (hash(team.name + "form") % 20 - 10)

        # 确保在 0-100 范围内
        attack_rating = max(0, min(100, attack_rating))
        defense_rating = max(0, min(100, defense_rating))
        midfield_rating = max(0, min(100, midfield_rating))
        form_rating = max(0, min(100, form_rating))

        return TeamStrengthResponse(
            team_id=team_id,
            team_name=team.name,
            overall_rating=overall_rating,
            attack_rating=attack_rating,
            defense_rating=defense_rating,
            midfield_rating=midfield_rating,
            form_rating=form_rating,
            ranking=fifa_ranking,
        )

"""AI Match Report Service"""

from anthropic import AsyncAnthropic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.match import Match
from app.models.team import Team


class AIMatchReportService:
    """AI-powered match report generation"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_report(self, match_id: int) -> dict:
        """Generate AI match report"""
        # Get match info
        result = await self.db.execute(select(Match).where(Match.id == match_id))
        match = result.scalar_one_or_none()
        if not match:
            raise ValueError(f"Match {match_id} not found")

        # Get team info
        team1_result = await self.db.execute(select(Team).where(Team.id == match.team1_id))
        team1 = team1_result.scalar_one_or_none()

        team2_result = await self.db.execute(select(Team).where(Team.id == match.team2_id))
        team2 = team2_result.scalar_one_or_none()

        if not team1 or not team2:
            raise ValueError("Teams not found")

        # Build prompt
        prompt = self._build_report_prompt(match, team1, team2)

        # Call Claude API
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )

        report_text = response.content[0].text

        return {
            "match_id": match_id,
            "team1_name": team1.name,
            "team2_name": team2.name,
            "score": f"{match.team1_score or 0}-{match.team2_score or 0}",
            "report": report_text,
            "highlights": self._extract_highlights(report_text),
        }

    def _build_report_prompt(self, match: Match, team1: Team, team2: Team) -> str:
        """Build match report prompt"""
        team1_stats = team1.stats or {}
        team2_stats = team2.stats or {}

        prompt = f"""你是一位专业的足球评论员。请为以下世界杯比赛撰写一份精彩的赛后评论。

比赛信息：
- 主队：{team1.name} vs 客队：{team2.name}
- 最终比分：{match.team1_score or 0}-{match.team2_score or 0}
- 阶段：{match.stage}
- 场地：{match.venue or "待定"}

{team1.name} 数据：
- FIFA 排名：{team1_stats.get("fifa_ranking", "N/A")}
- 教练：{team1.coach}

{team2.name} 数据：
- FIFA 排名：{team2_stats.get("fifa_ranking", "N/A")}
- 教练：{team2.coach}

请撰写一份 300-500 字的赛后评论，包括：
1. 比赛总体评价
2. 双方表现分析
3. 关键时刻和转折点
4. 球员表现亮点
5. 对后续比赛的展望

语气要专业、生动、引人入胜。"""

        return prompt

    def _extract_highlights(self, report: str) -> list[str]:
        """Extract key highlights from report"""
        # Simple extraction - in production, use NLP
        highlights = []
        lines = report.split("\n")

        for line in lines:
            if any(
                keyword in line for keyword in ["进球", "扑救", "关键", "精彩", "转折", "决定性"]
            ):
                if line.strip():
                    highlights.append(line.strip())

        return highlights[:5]  # Return top 5 highlights

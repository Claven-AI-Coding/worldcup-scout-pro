"""AI Prediction Service"""

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
    """AI Prediction Service"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def predict_match(self, match_id: int) -> MatchPredictionResponse:
        """Predict match result"""
        # Get match info
        result = await self.db.execute(
            select(Match).where(Match.id == match_id)
        )
        match = result.scalar_one_or_none()
        if not match:
            raise ValueError(f"Match {match_id} not found")

        # Get team info
        team1_result = await self.db.execute(
            select(Team).where(Team.id == match.team1_id)
        )
        team1 = team1_result.scalar_one_or_none()

        team2_result = await self.db.execute(
            select(Team).where(Team.id == match.team2_id)
        )
        team2 = team2_result.scalar_one_or_none()

        if not team1 or not team2:
            raise ValueError("Teams not found")

        # Build AI prompt
        prompt = self._build_prediction_prompt(match, team1, team2)

        # Call Claude API
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse AI response
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

    def _build_prediction_prompt(
        self, match: Match, team1: Team, team2: Team
    ) -> str:
        """Build prediction prompt"""
        team1_stats = team1.stats or {}
        team2_stats = team2.stats or {}

        prompt = f"""You are a professional football analyst. Please analyze the following World Cup match and provide a prediction.

Match Information:
- Home Team: {team1.name} ({team1.name_en})
- Away Team: {team2.name} ({team2.name_en})
- Stage: {match.stage}
- Venue: {match.venue or 'TBD'}

{team1.name} Data:
- FIFA Ranking: {team1_stats.get('fifa_ranking', 'N/A')}
- Confederation: {team1_stats.get('confederation', 'N/A')}
- World Cup Appearances: {team1_stats.get('appearances', 'N/A')}
- Best Result: {team1_stats.get('best_result', 'N/A')}
- Coach: {team1.coach}

{team2.name} Data:
- FIFA Ranking: {team2_stats.get('fifa_ranking', 'N/A')}
- Confederation: {team2_stats.get('confederation', 'N/A')}
- World Cup Appearances: {team2_stats.get('appearances', 'N/A')}
- Best Result: {team2_stats.get('best_result', 'N/A')}
- Coach: {team2.coach}

Please return the prediction in JSON format:
{{
  "team1_win_prob": 0.45,  // Home team win probability 0-1
  "draw_prob": 0.25,        // Draw probability 0-1
  "team2_win_prob": 0.30,   // Away team win probability 0-1
  "predicted_score": "2-1", // Predicted score
  "confidence": 0.75,       // Prediction confidence 0-1
  "key_factors": [          // Key factors (3-5 items)
    "Home team has higher FIFA ranking",
    "Away team in poor form",
    "Home advantage"
  ],
  "analysis": "Based on the comparison of both teams' strengths and historical data, the home team has a clear advantage..."  // 100-200 words analysis
}}

Note:
1. The sum of three probabilities must equal 1
2. Analysis should be objective and professional, based on data
3. Return JSON only, no other text
"""
        return prompt

    def _parse_ai_response(self, ai_text: str) -> dict[str, Any]:
        """Parse AI response"""
        try:
            # Extract JSON
            start = ai_text.find("{")
            end = ai_text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = ai_text[start:end]
                data = json.loads(json_str)

                # Validate probability sum
                total_prob = (
                    data["team1_win_prob"]
                    + data["draw_prob"]
                    + data["team2_win_prob"]
                )
                if abs(total_prob - 1.0) > 0.01:
                    # Normalize
                    data["team1_win_prob"] /= total_prob
                    data["draw_prob"] /= total_prob
                    data["team2_win_prob"] /= total_prob

                return data
        except Exception:
            pass

        # Parse failed, return default
        return {
            "team1_win_prob": 0.4,
            "draw_prob": 0.3,
            "team2_win_prob": 0.3,
            "predicted_score": "1-1",
            "confidence": 0.5,
            "key_factors": ["Insufficient data", "Need more information"],
            "analysis": "Due to limited data, the prediction is for reference only.",
        }

    async def get_team_strength(self, team_id: int) -> TeamStrengthResponse:
        """Get team strength assessment"""
        result = await self.db.execute(select(Team).where(Team.id == team_id))
        team = result.scalar_one_or_none()
        if not team:
            raise ValueError(f"Team {team_id} not found")

        stats = team.stats or {}
        fifa_ranking = stats.get("fifa_ranking", 50)

        # Calculate rating based on FIFA ranking (simplified algorithm)
        # Lower ranking (smaller number) = higher rating
        overall_rating = max(0, min(100, 100 - (fifa_ranking - 1) * 0.8))

        # Simulate ratings for each dimension (should be based on more data in production)
        attack_rating = overall_rating + (hash(team.name) % 20 - 10)
        defense_rating = overall_rating + (hash(team.name + "def") % 20 - 10)
        midfield_rating = overall_rating + (hash(team.name + "mid") % 20 - 10)
        form_rating = overall_rating + (hash(team.name + "form") % 20 - 10)

        # Ensure within 0-100 range
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

"""AI 预测相关 Schema"""

from pydantic import BaseModel, Field


class MatchPredictionRequest(BaseModel):
    """比赛预测请求"""

    match_id: int = Field(..., gt=0)


class MatchPredictionResponse(BaseModel):
    """比赛预测响应"""

    match_id: int
    team1_name: str
    team2_name: str
    team1_win_prob: float = Field(..., ge=0, le=1, description="主队胜率 0-1")
    draw_prob: float = Field(..., ge=0, le=1, description="平局概率 0-1")
    team2_win_prob: float = Field(..., ge=0, le=1, description="客队胜率 0-1")
    predicted_score: str = Field(..., description="预测比分，如 '2-1'")
    confidence: float = Field(..., ge=0, le=1, description="预测置信度 0-1")
    key_factors: list[str] = Field(default_factory=list, description="关键影响因素")
    analysis: str = Field(..., description="AI 分析文本")


class TeamStrengthResponse(BaseModel):
    """球队实力评估"""

    team_id: int
    team_name: str
    overall_rating: float = Field(..., ge=0, le=100, description="综合评分 0-100")
    attack_rating: float = Field(..., ge=0, le=100)
    defense_rating: float = Field(..., ge=0, le=100)
    midfield_rating: float = Field(..., ge=0, le=100)
    form_rating: float = Field(..., ge=0, le=100, description="近期状态")
    ranking: int = Field(..., gt=0, description="FIFA 排名")

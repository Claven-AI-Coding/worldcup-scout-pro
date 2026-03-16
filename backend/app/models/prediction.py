from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    match_id: Mapped[int] = mapped_column(Integer, ForeignKey("matches.id"), index=True)
    predicted_result: Mapped[str] = mapped_column(String(8))  # home, draw, away
    predicted_home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    predicted_away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    points_wagered: Mapped[int] = mapped_column(Integer, default=100)
    points_earned: Mapped[int | None] = mapped_column(Integer, nullable=True)
    settled: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="predictions")
    match = relationship("Match", back_populates="predictions")

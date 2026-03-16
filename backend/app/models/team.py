from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    name_en: Mapped[str | None] = mapped_column(String(64), nullable=True)
    code: Mapped[str] = mapped_column(String(8), unique=True)
    group_name: Mapped[str | None] = mapped_column(String(2), nullable=True)
    flag_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    coach: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    stats: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    players = relationship("Player", back_populates="team")
    fans = relationship("User", back_populates="fav_team")
    posts = relationship("Post", back_populates="team")
    home_matches = relationship(
        "Match", foreign_keys="Match.home_team_id", back_populates="home_team"
    )
    away_matches = relationship(
        "Match", foreign_keys="Match.away_team_id", back_populates="away_team"
    )

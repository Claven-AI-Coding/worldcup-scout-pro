from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BannedWord(Base):
    """违禁词库"""

    __tablename__ = "banned_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    word: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # profanity/gambling/political/spam
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

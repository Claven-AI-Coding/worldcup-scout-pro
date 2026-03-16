"""用户违规记录模型"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserViolation(Base):
    """用户违规记录"""

    __tablename__ = "user_violations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    violation_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # spam/profanity/harassment/illegal
    severity: Mapped[str] = mapped_column(String(20), default="warning")  # warning/serious/severe
    content: Mapped[str | None] = mapped_column(Text, nullable=True)  # 违规内容
    action_taken: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # warned/temp_ban/permanent_ban
    ban_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)  # 管理员备注
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="violations")

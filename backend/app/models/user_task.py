from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserTask(Base):
    """用户任务系统"""

    __tablename__ = "user_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    task_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # daily_sign_in/view_schedule/share/join_circle/predict
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    points_reward: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)  # 任务所属日期
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tasks")

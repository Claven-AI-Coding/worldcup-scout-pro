from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    openid: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(256), nullable=True)
    nickname: Mapped[str] = mapped_column(String(64), default="球迷")
    avatar: Mapped[str | None] = mapped_column(String(512), nullable=True)
    fav_team_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=1000)
    win_streak: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # 会员相关字段
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_member: Mapped[bool] = mapped_column(Boolean, default=False)
    member_expire_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    member_type: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # monthly/quarterly/yearly
    daily_sign_in: Mapped[date | None] = mapped_column(Date, nullable=True)  # 最后签到日期
    sign_in_streak: Mapped[int] = mapped_column(Integer, default=0)  # 连续签到天数
    badges: Mapped[list | None] = mapped_column(JSONB, server_default="[]")  # 勋章列表
    agreed_terms: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否同意协议
    # 封禁相关字段
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否被封禁
    ban_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )  # 封禁到期时间（None 表示永久封禁）
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    fav_team = relationship("Team", back_populates="fans")
    posts = relationship("Post", back_populates="author")
    predictions = relationship("Prediction", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    wallpapers = relationship("Wallpaper", back_populates="user")
    point_records = relationship("PointRecord", back_populates="user")
    tasks = relationship("UserTask", back_populates="user")
    reports = relationship("Report", back_populates="reporter")
    violations = relationship("UserViolation", back_populates="user")


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    match_id: Mapped[int] = mapped_column(Integer, ForeignKey("matches.id"))
    remind_before_minutes: Mapped[int] = mapped_column(Integer, default=30)
    sent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="reminders")
    match = relationship("Match", back_populates="reminders")

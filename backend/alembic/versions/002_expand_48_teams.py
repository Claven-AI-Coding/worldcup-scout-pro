"""Expand to 48 teams, add compliance/task/member tables

Revision ID: 002
Revises: 001
Create Date: 2026-03-03
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---- users 表新增字段 ----
    op.add_column("users", sa.Column("phone", sa.String(20), nullable=True))
    op.add_column(
        "users",
        sa.Column("is_member", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "users", sa.Column("member_expire_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "users", sa.Column("member_type", sa.String(20), nullable=True)
    )  # monthly/quarterly/yearly
    op.add_column(
        "users", sa.Column("daily_sign_in", sa.Date(), nullable=True)
    )  # 最后签到日期
    op.add_column(
        "users",
        sa.Column("sign_in_streak", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "users",
        sa.Column("badges", postgresql.JSONB(), server_default="[]", nullable=True),
    )
    op.add_column(
        "users",
        sa.Column(
            "agreed_terms", sa.Boolean(), nullable=False, server_default="false"
        ),
    )

    # ---- 积分流水记录 ----
    op.create_table(
        "point_records",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(50), nullable=False),
        sa.Column("detail", sa.String(200), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index("ix_point_records_id", "point_records", ["id"])
    op.create_index("ix_point_records_user_id", "point_records", ["user_id"])

    # ---- 用户任务系统 ----
    op.create_table(
        "user_tasks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("task_type", sa.String(50), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("points_reward", sa.Integer(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index("ix_user_tasks_id", "user_tasks", ["id"])
    op.create_index("ix_user_tasks_user_id", "user_tasks", ["user_id"])

    # ---- 举报记录 ----
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "reporter_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column("target_type", sa.String(20), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(200), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index("ix_reports_id", "reports", ["id"])
    op.create_index("ix_reports_reporter_id", "reports", ["reporter_id"])

    # ---- 违禁词库 ----
    op.create_table(
        "banned_words",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("word", sa.String(100), unique=True, nullable=False),
        sa.Column("category", sa.String(50), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index("ix_banned_words_id", "banned_words", ["id"])


def downgrade() -> None:
    op.drop_table("banned_words")
    op.drop_table("reports")
    op.drop_table("user_tasks")
    op.drop_table("point_records")

    op.drop_column("users", "agreed_terms")
    op.drop_column("users", "badges")
    op.drop_column("users", "sign_in_streak")
    op.drop_column("users", "daily_sign_in")
    op.drop_column("users", "member_type")
    op.drop_column("users", "member_expire_at")
    op.drop_column("users", "is_member")
    op.drop_column("users", "phone")

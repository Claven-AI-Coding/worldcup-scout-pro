"""add user ban fields and user_violations table

Revision ID: 003
Revises: 002
Create Date: 2026-03-13 12:30:00

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加用户封禁字段
    op.add_column("users", sa.Column("is_banned", sa.Boolean(), server_default="false", nullable=False))
    op.add_column("users", sa.Column("ban_until", sa.DateTime(timezone=True), nullable=True))

    # 创建用户违规记录表
    op.create_table(
        "user_violations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("violation_type", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=20), server_default="warning", nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("action_taken", sa.String(length=50), nullable=True),
        sa.Column("ban_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_violations_user_id"), "user_violations", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_violations_user_id"), table_name="user_violations")
    op.drop_table("user_violations")
    op.drop_column("users", "ban_until")
    op.drop_column("users", "is_banned")

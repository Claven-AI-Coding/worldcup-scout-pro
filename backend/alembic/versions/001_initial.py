"""Initial migration - create all tables

Revision ID: 001
Revises: None
Create Date: 2026-03-02
"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Teams
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(64), unique=True, nullable=False),
        sa.Column("name_en", sa.String(64), nullable=True),
        sa.Column("code", sa.String(8), unique=True, nullable=False),
        sa.Column("group_name", sa.String(2), nullable=True),
        sa.Column("flag_url", sa.String(512), nullable=True),
        sa.Column("coach", sa.String(64), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("stats", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_teams_id", "teams", ["id"])

    # Users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("openid", sa.String(128), unique=True, nullable=True),
        sa.Column("username", sa.String(64), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(256), nullable=True),
        sa.Column("nickname", sa.String(64), nullable=False, server_default="球迷"),
        sa.Column("avatar", sa.String(512), nullable=True),
        sa.Column("fav_team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=True),
        sa.Column("points", sa.Integer(), nullable=False, server_default="1000"),
        sa.Column("win_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("title", sa.String(32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_username", "users", ["username"])

    # Players
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("name_en", sa.String(64), nullable=True),
        sa.Column("number", sa.Integer(), nullable=True),
        sa.Column("position", sa.String(16), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("club", sa.String(64), nullable=True),
        sa.Column("photo_url", sa.String(512), nullable=True),
        sa.Column("stats", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_players_id", "players", ["id"])
    op.create_index("ix_players_team_id", "players", ["team_id"])

    # Matches
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("stage", sa.String(32), nullable=False),
        sa.Column("group_name", sa.String(2), nullable=True),
        sa.Column("home_team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("away_team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="upcoming"),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("venue", sa.String(128), nullable=True),
        sa.Column("matchday", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_matches_id", "matches", ["id"])

    # Match Events
    op.create_table(
        "match_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("match_id", sa.Integer(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("event_type", sa.String(16), nullable=False),
        sa.Column("minute", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), sa.ForeignKey("players.id"), nullable=True),
        sa.Column("detail", sa.String(256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_match_events_id", "match_events", ["id"])
    op.create_index("ix_match_events_match_id", "match_events", ["match_id"])

    # Posts
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("images", postgresql.JSONB(), nullable=True),
        sa.Column("likes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("comments_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_posts_id", "posts", ["id"])
    op.create_index("ix_posts_user_id", "posts", ["user_id"])
    op.create_index("ix_posts_team_id", "posts", ["team_id"])

    # Comments
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_comments_id", "comments", ["id"])
    op.create_index("ix_comments_post_id", "comments", ["post_id"])

    # Predictions
    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("match_id", sa.Integer(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("predicted_result", sa.String(8), nullable=False),
        sa.Column("predicted_home_score", sa.Integer(), nullable=True),
        sa.Column("predicted_away_score", sa.Integer(), nullable=True),
        sa.Column("points_wagered", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("points_earned", sa.Integer(), nullable=True),
        sa.Column("settled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_predictions_id", "predictions", ["id"])
    op.create_index("ix_predictions_user_id", "predictions", ["user_id"])
    op.create_index("ix_predictions_match_id", "predictions", ["match_id"])

    # Wallpapers
    op.create_table(
        "wallpapers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=True),
        sa.Column("player_id", sa.Integer(), sa.ForeignKey("players.id"), nullable=True),
        sa.Column("style", sa.String(32), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("image_url", sa.String(512), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_wallpapers_id", "wallpapers", ["id"])
    op.create_index("ix_wallpapers_user_id", "wallpapers", ["user_id"])

    # Reminders
    op.create_table(
        "reminders",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("match_id", sa.Integer(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("remind_before_minutes", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("sent", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_reminders_id", "reminders", ["id"])


def downgrade() -> None:
    op.drop_table("reminders")
    op.drop_table("wallpapers")
    op.drop_table("predictions")
    op.drop_table("comments")
    op.drop_table("posts")
    op.drop_table("match_events")
    op.drop_table("matches")
    op.drop_table("players")
    op.drop_table("users")
    op.drop_table("teams")

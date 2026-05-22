"""add parsed pages table

Revision ID: 20260522_0002
Revises: 20260522_0001
Create Date: 2026-05-22 17:35:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260522_0002"
down_revision = "20260522_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "parsed_pages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("concurrency_mode", sa.String(length=20), nullable=False),
        sa.Column("http_status_code", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.String(length=500), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_parsed_pages_url"), "parsed_pages", ["url"], unique=False)
    op.create_index(
        op.f("ix_parsed_pages_concurrency_mode"),
        "parsed_pages",
        ["concurrency_mode"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_parsed_pages_concurrency_mode"), table_name="parsed_pages")
    op.drop_index(op.f("ix_parsed_pages_url"), table_name="parsed_pages")
    op.drop_table("parsed_pages")

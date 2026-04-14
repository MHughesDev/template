# apps/api/alembic/versions/b1d2e3f4a5b6_add_examples_table.py
"""add examples table

Revision ID: b1d2e3f4a5b6
Revises: a9c49fe6e44e
Create Date: 2026-04-14

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b1d2e3f4a5b6"
down_revision: str | None = "a9c49fe6e44e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "examples",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("examples")

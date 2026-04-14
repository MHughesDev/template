# apps/api/alembic/versions/c2d3e4f5a6b7_add_example_owner_user_id.py
"""add owner_user_id to examples for per-user isolation

Revision ID: c2d3e4f5a6b7
Revises: b1d2e3f4a5b6
Create Date: 2026-04-14

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c2d3e4f5a6b7"
down_revision: str | None = "b1d2e3f4a5b6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "examples",
        sa.Column("owner_user_id", sa.Uuid(), nullable=True),
    )
    op.create_foreign_key(
        "fk_examples_owner_user_id_users",
        "examples",
        "users",
        ["owner_user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        "ix_examples_owner_user_id",
        "examples",
        ["owner_user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_examples_owner_user_id", table_name="examples")
    op.drop_constraint(
        "fk_examples_owner_user_id_users", "examples", type_="foreignkey"
    )
    op.drop_column("examples", "owner_user_id")

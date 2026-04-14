# apps/api/alembic/versions/c2d3e4f5a6b7_add_example_owner_user_id.py
"""add owner_user_id to examples for per-user isolation

Revision ID: c2d3e4f5a6b7
Revises: b1d2e3f4a5b6
Create Date: 2026-04-14

SQLite: FK/index adds use ``batch_alter_table`` with ``copy_from=`` so offline
``alembic upgrade --sql`` does not require a live DB (CI migrate-dry-run).

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import context as alembic_context
from alembic import op

revision: str = "c2d3e4f5a6b7"
down_revision: str | None = "b1d2e3f4a5b6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Pre-migration ``examples`` shape (must match b1d2e3f4a5b6) for SQLite batch copy.
_examples_before = sa.Table(
    "examples",
    sa.MetaData(),
    sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
    sa.Column("title", sa.String(length=255), nullable=False),
    sa.Column("description", sa.Text(), nullable=True),
    sa.Column("status", sa.String(length=50), nullable=False),
    sa.Column("tenant_id", sa.Uuid(), nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)

# Post-upgrade shape for SQLite downgrade batch copy.
_examples_after = sa.Table(
    "examples",
    sa.MetaData(),
    sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
    sa.Column("title", sa.String(length=255), nullable=False),
    sa.Column("description", sa.Text(), nullable=True),
    sa.Column("status", sa.String(length=50), nullable=False),
    sa.Column("tenant_id", sa.Uuid(), nullable=True),
    sa.Column("owner_user_id", sa.Uuid(), nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)


def _is_sqlite() -> bool:
    bind = op.get_bind()
    if bind is not None:
        return bind.dialect.name == "sqlite"
    ctx = alembic_context.get_context()
    dialect = getattr(ctx, "dialect", None)
    if dialect is not None:
        return dialect.name == "sqlite"
    return False


def upgrade() -> None:
    if _is_sqlite():
        with op.batch_alter_table(
            "examples", schema=None, copy_from=_examples_before
        ) as batch_op:
            batch_op.add_column(sa.Column("owner_user_id", sa.Uuid(), nullable=True))
            batch_op.create_foreign_key(
                "fk_examples_owner_user_id_users",
                "users",
                ["owner_user_id"],
                ["id"],
                ondelete="CASCADE",
            )
            batch_op.create_index(
                "ix_examples_owner_user_id",
                ["owner_user_id"],
                unique=False,
            )
        return

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
    if _is_sqlite():
        with op.batch_alter_table(
            "examples", schema=None, copy_from=_examples_after
        ) as batch_op:
            batch_op.drop_index("ix_examples_owner_user_id")
            batch_op.drop_constraint(
                "fk_examples_owner_user_id_users",
                type_="foreignkey",
            )
            batch_op.drop_column("owner_user_id")
        return

    op.drop_index("ix_examples_owner_user_id", table_name="examples")
    op.drop_constraint(
        "fk_examples_owner_user_id_users", "examples", type_="foreignkey"
    )
    op.drop_column("examples", "owner_user_id")

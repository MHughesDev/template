## apps/api/alembic/script.py.mako
## BLUEPRINT: Composer 2 implements from this structure
## PURPOSE: Alembic migration script template. Standard Mako template for generating
##          migration files with file title comment, revision ID, and up/down functions.
##          Per spec §26.8 item 210.

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

## EXPAND/CONTRACT PHASE: TODO — document whether this is an expand, contract, or single-phase migration
## ROLLBACK PLAN: TODO — document how to rollback this migration safely
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Apply the migration. Write explicit operations, do not rely on autogenerate entirely.

    STEPS:
    1. Describe each operation
    2. Verify safe order (foreign keys, indexes)
    """
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Reverse the migration. Must be the exact inverse of upgrade().

    STEPS:
    1. Reverse each upgrade operation in reverse order
    """
    ${downgrades if downgrades else "pass"}

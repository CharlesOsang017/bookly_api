"""Fix password hash column type

Revision ID: f3a7c9d2e114
Revises: c0c41b085961
Create Date: 2026-09-11

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f3a7c9d2e114"
down_revision: Union[str, Sequence[str], None] = "c0c41b085961"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "Users",
        "password_hash",
        existing_type=sa.Boolean(),
        type_=sa.String(),
        existing_nullable=False,
        postgresql_using="password_hash::text",
    )


def downgrade() -> None:
    op.alter_column(
        "Users",
        "password_hash",
        existing_type=sa.String(),
        type_=sa.Boolean(),
        existing_nullable=False,
        postgresql_using="false",
    )

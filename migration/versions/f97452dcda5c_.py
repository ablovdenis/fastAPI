"""empty message

Revision ID: f97452dcda5c
Revises: f741232a2c56
Create Date: 2026-03-30 20:21:07.453859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f97452dcda5c'
down_revision: Union[str, Sequence[str], None] = 'f741232a2c56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""new

Revision ID: 5b8d4428fa2e
Revises: f07f0d842f3e
Create Date: 2025-11-09 18:04:14.108712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b8d4428fa2e'
down_revision: Union[str, Sequence[str], None] = 'f07f0d842f3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

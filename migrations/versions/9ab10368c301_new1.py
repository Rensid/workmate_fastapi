"""new1

Revision ID: 9ab10368c301
Revises: 5b8d4428fa2e
Create Date: 2025-11-09 18:04:40.133183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ab10368c301'
down_revision: Union[str, Sequence[str], None] = '5b8d4428fa2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

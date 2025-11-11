"""new2

Revision ID: e0cc13b1ee2c
Revises: 9ab10368c301
Create Date: 2025-11-09 18:11:26.965675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0cc13b1ee2c'
down_revision: Union[str, Sequence[str], None] = '9ab10368c301'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""subcategoria_id nullable

Revision ID: 9589fc0ed5ba
Revises: 4fe10c85f5bf
Create Date: 2025-04-29 23:32:30.682281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9589fc0ed5ba'
down_revision: Union[str, None] = '4fe10c85f5bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

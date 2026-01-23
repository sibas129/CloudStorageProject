"""test admin

Revision ID: 5803b6d475d4
Revises: a10b5620be8c
Create Date: 2024-12-01 22:35:59.462383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5803b6d475d4'
down_revision: Union[str, None] = 'a10b5620be8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

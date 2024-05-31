"""Admin field added

Revision ID: 1e090585c806
Revises: d6b0447465de
Create Date: 2024-05-31 10:30:23.279365

"""
from typing import Sequence, Union
import sqlmodel

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e090585c806'
down_revision: Union[str, None] = 'd6b0447465de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appuser', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('appuser', 'is_admin')
    # ### end Alembic commands ###

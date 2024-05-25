"""add travel_together nodel

Revision ID: cbd42a9fffe6
Revises: c7b6c3188f65
Create Date: 2024-05-17 17:04:22.110020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision: str = 'cbd42a9fffe6'
down_revision: Union[str, None] = 'c7b6c3188f65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('traveltogether', sa.Column('comment', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('traveltogether', 'comment')
    # ### end Alembic commands ###

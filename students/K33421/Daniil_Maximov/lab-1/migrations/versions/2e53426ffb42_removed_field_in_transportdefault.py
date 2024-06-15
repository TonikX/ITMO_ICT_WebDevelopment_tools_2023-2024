"""removed field in transportDefault

Revision ID: 2e53426ffb42
Revises: 
Create Date: 2024-06-10 10:57:09.060667

"""
from typing import Sequence, Union

from alembic import op
from sqlmodel import SQLModel
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e53426ffb42'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transport', sa.Column('test', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transport', 'test')
    # ### end Alembic commands ###

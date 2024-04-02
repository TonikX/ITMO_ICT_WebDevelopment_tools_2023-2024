"""fix genre

Revision ID: 65b07b118c83
Revises: ec9d28f4ff23
Create Date: 2024-04-01 21:51:39.843618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '65b07b118c83'
down_revision: Union[str, None] = 'ec9d28f4ff23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'genre',
               existing_type=postgresql.ENUM('Fiction', 'NonFiction', 'Mystery', 'Romance', 'ScienceFiction', name='bookgenre'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'genre',
               existing_type=postgresql.ENUM('Fiction', 'NonFiction', 'Mystery', 'Romance', 'ScienceFiction', name='bookgenre'),
               nullable=True)
    # ### end Alembic commands ###

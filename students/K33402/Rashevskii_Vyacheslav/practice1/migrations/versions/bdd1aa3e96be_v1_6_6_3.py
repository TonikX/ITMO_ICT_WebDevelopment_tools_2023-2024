"""v1.6.6.3

Revision ID: bdd1aa3e96be
Revises: 1137666a81f1
Create Date: 2024-05-06 22:57:02.436248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bdd1aa3e96be'
down_revision: Union[str, None] = '1137666a81f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

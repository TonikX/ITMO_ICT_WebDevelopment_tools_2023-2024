"""skill added

Revision ID: 7b553d50013c
Revises: a9013c53c805
Create Date: 2024-03-23 16:52:53.221951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7b553d50013c'
down_revision: Union[str, None] = 'a9013c53c805'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('user', sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'password')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###

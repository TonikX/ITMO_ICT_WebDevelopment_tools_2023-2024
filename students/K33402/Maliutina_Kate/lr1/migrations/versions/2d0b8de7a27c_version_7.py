"""version 7

Revision ID: 2d0b8de7a27c
Revises: 34a78eb678ae
Create Date: 2024-06-02 21:56:37.206443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2d0b8de7a27c'
down_revision: Union[str, None] = '34a78eb678ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index('ix_customer_username', table_name='customer')
    # op.drop_table('customer')
    # op.drop_table('transaction')
    # op.drop_table('categoryoperationlink')
    # op.drop_table('operation')
    # op.drop_table('category')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('category_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('limit', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('current', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='category_pkey'),
    sa.UniqueConstraint('category', name='category_category_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('operation',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('operation_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('operation', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('limit', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('alias', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='operation_pkey'),
    sa.UniqueConstraint('operation', name='operation_operation_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('categoryoperationlink',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('operation_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name='categoryoperationlink_category_id_fkey'),
    sa.ForeignKeyConstraint(['operation_id'], ['operation.id'], name='categoryoperationlink_operation_id_fkey'),
    sa.PrimaryKeyConstraint('id', 'category_id', 'operation_id', name='categoryoperationlink_pkey'),
    sa.UniqueConstraint('id', name='categoryoperationlink_id_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('transaction',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('category_operation_link_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_operation_link_id'], ['categoryoperationlink.id'], name='transaction_category_operation_link_id_fkey'),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], name='transaction_customer_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='transaction_pkey')
    )
    op.create_table('customer',
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('favourite_category_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('balance', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['favourite_category_id'], ['category.id'], name='customer_favourite_category_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='customer_pkey')
    )
    op.create_index('ix_customer_username', 'customer', ['username'], unique=True)
    # ### end Alembic commands ###

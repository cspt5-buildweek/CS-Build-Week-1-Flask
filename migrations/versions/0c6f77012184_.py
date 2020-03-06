"""empty message

Revision ID: 0c6f77012184
Revises: 0848d2ffb287
Create Date: 2020-03-04 23:29:20.069951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c6f77012184'
down_revision = '0848d2ffb287'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    op.create_table('inventory_items',
    sa.Column('inventory_id', sa.Integer(), nullable=True),
    sa.Column('items_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.ForeignKeyConstraint(['items_id'], ['items.id'], )
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['inventory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('inventory', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'inventory', ['inventory'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'inventory')
    op.drop_table('items')
    op.drop_table('inventory_items')
    op.drop_table('inventory')
    # ### end Alembic commands ###

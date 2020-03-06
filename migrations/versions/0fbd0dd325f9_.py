"""empty message

Revision ID: 0fbd0dd325f9
Revises: 
Create Date: 2020-03-06 00:54:45.885492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fbd0dd325f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('nodes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory_items',
    sa.Column('inventory_id', sa.Integer(), nullable=False),
    sa.Column('items_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.ForeignKeyConstraint(['items_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('inventory_id', 'items_id')
    )
    op.create_table('links',
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('source_direction', sa.String(), nullable=False),
    sa.Column('target_direction', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['source_id'], ['nodes.id'], ),
    sa.ForeignKeyConstraint(['target_id'], ['nodes.id'], ),
    sa.PrimaryKeyConstraint('source_id', 'target_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('starting_room', sa.Integer(), nullable=True),
    sa.Column('inventory', sa.Integer(), nullable=True),
    sa.Column('coin_pouch', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inventory'], ['inventory.id'], ),
    sa.ForeignKeyConstraint(['starting_room'], ['nodes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('links')
    op.drop_table('inventory_items')
    op.drop_table('nodes')
    op.drop_table('items')
    op.drop_table('inventory')
    # ### end Alembic commands ###

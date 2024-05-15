"""empty message

Revision ID: 22be14cadf26
Revises: 
Create Date: 2024-05-14 20:43:38.743349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22be14cadf26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.String(length=5), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.String(length=5), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_movement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movement_id', sa.String(length=5), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('from_location_id', sa.String(length=5), nullable=True),
    sa.Column('to_location_id', sa.String(length=5), nullable=True),
    sa.Column('product_id', sa.String(length=5), nullable=False),
    sa.Column('qty', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['from_location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['to_location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_movement')
    op.drop_table('products')
    op.drop_table('locations')
    # ### end Alembic commands ###

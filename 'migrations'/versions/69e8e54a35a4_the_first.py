"""'the_first'

Revision ID: 69e8e54a35a4
Revises: 
Create Date: 2023-07-09 19:53:22.063728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69e8e54a35a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('registred', sa.TIMESTAMP(), nullable=True),
    sa.Column('hashed_password', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('cards', sa.ARRAY(sa.BigInteger()), nullable=True),
    sa.Column('cart', sa.JSON(), nullable=True),
    sa.Column('discounts', sa.JSON(), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('tags', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('seller', sa.Integer(), nullable=True),
    sa.Column('quanity', sa.Integer(), nullable=False),
    sa.Column('discount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['seller'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('users')
    # ### end Alembic commands ###

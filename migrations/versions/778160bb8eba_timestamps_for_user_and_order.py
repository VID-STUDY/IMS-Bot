"""Timestamps for user and order

Revision ID: 778160bb8eba
Revises: 2eab259d11f5
Create Date: 2019-05-13 13:08:22.582694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '778160bb8eba'
down_revision = '2eab259d11f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ad_campaigns', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('registered_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'registered_at')
    op.drop_column('ad_campaigns', 'confirmed_at')
    # ### end Alembic commands ###

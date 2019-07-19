"""empty message

Revision ID: 6fc9e426e339
Revises: 778160bb8eba
Create Date: 2019-06-09 02:59:18.497177

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6fc9e426e339'
down_revision = '778160bb8eba'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('rating', sa.Column('image_id', sa.String(length=120), nullable=True))
    op.add_column('rating', sa.Column('image_path', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rating', 'image_path')
    op.drop_column('rating', 'image_id')
    # ### end Alembic commands ###

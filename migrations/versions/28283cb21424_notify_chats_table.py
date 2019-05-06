"""Notify chats table

Revision ID: 28283cb21424
Revises: 39cab1b8f985
Create Date: 2019-05-06 15:16:51.465366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28283cb21424'
down_revision = '39cab1b8f985'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notify_chats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notify_chats')
    # ### end Alembic commands ###

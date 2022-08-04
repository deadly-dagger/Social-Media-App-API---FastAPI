"""add content column to post table

Revision ID: 66b200446edd
Revises: fcd1332c3151
Create Date: 2022-08-04 20:31:15.096196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66b200446edd'
down_revision = 'fcd1332c3151'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

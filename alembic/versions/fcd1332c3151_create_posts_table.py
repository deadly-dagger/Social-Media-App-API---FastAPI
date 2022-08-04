"""create posts table

Revision ID: fcd1332c3151
Revises: 
Create Date: 2022-08-04 20:28:55.503079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcd1332c3151'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass

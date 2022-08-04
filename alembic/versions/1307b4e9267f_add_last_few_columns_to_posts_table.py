"""add last few columns to posts table

Revision ID: 1307b4e9267f
Revises: 482c3e2f59a7
Create Date: 2022-08-04 20:35:22.582810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1307b4e9267f'
down_revision = '482c3e2f59a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

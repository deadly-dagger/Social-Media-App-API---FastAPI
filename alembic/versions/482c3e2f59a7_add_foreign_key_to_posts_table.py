"""add foreign key to posts table

Revision ID: 482c3e2f59a7
Revises: c154024a37ff
Create Date: 2022-08-04 20:34:25.402498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '482c3e2f59a7'
down_revision = 'c154024a37ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass

"""adding foreign key to stories

Revision ID: 7fd52dba5330
Revises: aef298b004d8
Create Date: 2021-11-13 12:35:34.733246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fd52dba5330'
down_revision = 'aef298b004d8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('stories', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('story_users_fk', source_table="stories" ,referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('story_users_fk', table_name="stories")
    op.drop_column('stories', 'owner_id')
    pass

"""create story_table

Revision ID: 2c43b68002fc
Revises: 
Create Date: 2021-11-12 22:39:00.146995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c43b68002fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('stories',
                    sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
                    )
    pass


def downgrade():
    op.drop_table('stories')
    pass

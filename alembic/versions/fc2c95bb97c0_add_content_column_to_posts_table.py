"""add content column to posts table

Revision ID: fc2c95bb97c0
Revises: ad815d5a1b2d
Create Date: 2023-07-29 12:01:57.260507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc2c95bb97c0'
down_revision = 'ad815d5a1b2d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

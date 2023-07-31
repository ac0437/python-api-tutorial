"""add user table

Revision ID: 609a48c7496a
Revises: fc2c95bb97c0
Create Date: 2023-07-29 12:09:14.784435

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as sau

# revision identifiers, used by Alembic.
revision = '609a48c7496a'
down_revision = 'fc2c95bb97c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('email', sau.EmailType,
                              nullable=False, unique=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass

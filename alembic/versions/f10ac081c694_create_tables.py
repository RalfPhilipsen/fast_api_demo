"""create tables

Revision ID: f10ac081c694
Revises: 
Create Date: 2021-10-29 14:43:57.360992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f10ac081c694'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False, unique=True)
    )

    op.create_table(
        'garments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('brand_name', sa.String(50), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('color', sa.String(50), nullable=False),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('garments')

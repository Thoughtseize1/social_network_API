"""Add created_at to user_likes table

Revision ID: 10cb0424aee2
Revises: 2e3b42054b86
Create Date: 2023-12-29 17:31:30.394123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10cb0424aee2'
down_revision: Union[str, None] = '2e3b42054b86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_likes', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_likes', 'created_at')
    # ### end Alembic commands ###

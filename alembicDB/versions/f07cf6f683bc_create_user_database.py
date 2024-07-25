"""create user database

Revision ID: f07cf6f683bc
Revises: 4d0de6b9af68
Create Date: 2024-07-08 20:48:15.172982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f07cf6f683bc'
down_revision: Union[str, None] = '4d0de6b9af68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("borrowers",
                    sa.Column('borrower_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('password',sa.String(length=255),nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('borrowers')
    pass

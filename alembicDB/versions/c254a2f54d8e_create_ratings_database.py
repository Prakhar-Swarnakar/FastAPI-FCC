"""create ratings database

Revision ID: c254a2f54d8e
Revises: 957cb5c4dc6e
Create Date: 2024-07-17 14:25:14.194925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c254a2f54d8e'
down_revision: Union[str, None] = '957cb5c4dc6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("ratings",
                    sa.Column('book_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('borrower_id', sa.Integer(), nullable=False),
                    sa.Column('rating', sa.Integer(), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('ratings')
    pass

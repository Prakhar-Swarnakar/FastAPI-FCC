"""create transaction  database

Revision ID: bc653025a09e
Revises: f07cf6f683bc
Create Date: 2024-07-17 13:58:58.120672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc653025a09e'
down_revision: Union[str, None] = 'f07cf6f683bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("transactions",
                    sa.Column('transactionID', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('book_Id', sa.Integer(), nullable=False),
                    sa.Column('borrower_id', sa.Integer(), nullable=False),
                    sa.Column('borrow_date', sa.DATE(), nullable=False),
                    sa.Column('return_date', sa.DATE(), nullable=True),
                    sa.Column('returned', sa.Boolean(), nullable=False),
                    sa.Column('Upvote', sa.Boolean(), nullable=True)
                    )
    pass


def downgrade() -> None:
    op.drop_table('transactions')
    pass

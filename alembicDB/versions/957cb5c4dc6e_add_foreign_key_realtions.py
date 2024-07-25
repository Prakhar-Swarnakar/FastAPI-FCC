"""add foreign-key realtions

Revision ID: 957cb5c4dc6e
Revises: bc653025a09e
Create Date: 2024-07-08 20:53:20.419997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '957cb5c4dc6e'
down_revision: Union[str, None] = 'bc653025a09e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key('fk_transaction_books', source_table='transactions', referent_table='books',
                          local_cols=['book_Id'], remote_cols=['book_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_transaction_borrowers', source_table='transactions', referent_table='borrowers',
                          local_cols= ['borrower_id'], remote_cols=['borrower_id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('fk_transaction_books', table_name='transactions', type_='foreignkey')
    op.drop_constraint('fk_transaction_borrowers', table_name='transactions', type_='foreignkey')
    pass

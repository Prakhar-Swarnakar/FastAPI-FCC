"""create book database

Revision ID: 4d0de6b9af68
Revises: 
Create Date: 2024-07-02 12:58:57.751903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d0de6b9af68'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_table(
        "books",
        sa.Column('book_id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),  # Assuming max length of 255
        sa.Column('genre', sa.String(length=255), nullable=False),  # Assuming max length of 255
        sa.Column('available_issues', sa.Integer(), nullable=False),
        sa.Column('available', sa.Boolean(), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, default=True)
    )
    pass

def downgrade():
    op.drop_table('books')
    pass

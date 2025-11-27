"""Add ingestion_logs table

Revision ID: ae62dc0bf4ea
Revises: a6cf325e842e
Create Date: 2025-11-27 15:19:43.351594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae62dc0bf4ea'
down_revision: Union[str, Sequence[str], None] = 'a6cf325e842e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ingestion_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("query", sa.String(), nullable=False),
        sa.Column("pages_processed", sa.Integer(), nullable=False),
        sa.Column("papers_added", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ingestion_logs")

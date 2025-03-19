"""create_books_table

Revision ID: b1f3b465e75a
Revises:
Create Date: 2025-03-19 11:43:12.140391

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b1f3b465e75a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

  op.execute("""
    CREATE TABLE books (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      title VARCHAR NOT NULL,
      authors JSONB NOT NULL,
      summaries JSONB,
      translators JSONB,
      subjects JSONB,
      bookshelves JSONB,
      languages JSONB,
      created_timestamp TIMESTAMPTZ DEFAULT now() NOT NULL,
      updated_timestamp TIMESTAMPTZ DEFAULT now() NOT NULL,
      deleted_timestamp TIMESTAMPTZ
    );
  """)


def downgrade() -> None:
  op.execute("DROP TABLE books;")
  op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')

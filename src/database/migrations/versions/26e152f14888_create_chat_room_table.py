"""create_chat_room_table

Revision ID: 26e152f14888
Revises: b1f3b465e75a
Create Date: 2025-03-30 18:54:56.693413

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '26e152f14888'
down_revision: Union[str, None] = 'b1f3b465e75a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.execute("""
    CREATE TABLE chat_rooms (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      name VARCHAR NOT NULL,
      created_at TIMESTAMPTZ DEFAULT now() NOT NULL,

      CONSTRAINT uq_chat_room_name UNIQUE (name)
    );
  """)


def downgrade() -> None:
  op.execute("DROP TABLE chat_rooms;")

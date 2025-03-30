"""create_chat_room_messages_table

Revision ID: 138fc8b5488e
Revises: 26e152f14888
Create Date: 2025-03-30 18:57:10.467561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '138fc8b5488e'
down_revision: Union[str, None] = '26e152f14888'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.execute("""
    CREATE TABLE chat_room_messages (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      chat_room_id UUID,
      username VARCHAR NOT NULL,
      message TEXT NOT NULL,
      created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
      
      CONSTRAINT fk_chat_room_messages_chat_room_id FOREIGN KEY (chat_room_id)
      REFERENCES chat_rooms (id) ON DELETE CASCADE
    );
  """)


def downgrade() -> None:
  op.execute("DROP TABLE chat_room_messages;")

from sqlalchemy import text

from src.database import engine


def create_conversation() -> int:
    sql = text(
        """
        INSERT INTO conversations (created_at)
        VALUES (CURRENT_TIMESTAMP)
        RETURNING id
        """
    )

    with engine.begin() as connection:
        result = connection.execute(sql)
        conversation_id = result.scalar_one()

    return conversation_id

def save_message(
    conversation_id: int,
    role: str,
    content: str,
) -> None:
    sql = text(
        """
        INSERT INTO messages (
            conversation_id,
            role,
            content,
            created_at
        )
        VALUES (
            :conversation_id,
            :role,
            :content,
            CURRENT_TIMESTAMP
        )
        """
    )

    with engine.begin() as connection:
        connection.execute(
            sql,
            {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
            },
        )


def get_messages(conversation_id: int) -> list[dict]:
    sql = text(
        """
        SELECT
            role,
            content
        FROM messages
        WHERE conversation_id = :conversation_id
        ORDER BY created_at ASC, id ASC
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            sql,
            {
                "conversation_id": conversation_id,
            },
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]
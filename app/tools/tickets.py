from langchain_core.tools import tool
from sqlalchemy import text

from src.database import engine


@tool
def create_support_ticket(
    title: str,
    description: str,
    customer_message: str,
) -> str:
    """
    Create a new support ticket in the customer support database.

    Use this tool when the customer explicitly wants
    to create a support ticket.
    """

    sql = text(
        """
        INSERT INTO tickets (
            title,
            description,
            customer_message,
            status,
            created_at
        )
        VALUES (
            :title,
            :description,
            :customer_message,
            'OPEN',
            CURRENT_TIMESTAMP
        )
        RETURNING id
        """
    )

    with engine.begin() as connection:
        result = connection.execute(
            sql,
            {
                "title": title,
                "description": description,
                "customer_message": customer_message,
            },
        )

        ticket_id = result.scalar_one()

    return f"Support ticket #{ticket_id} has been created successfully."
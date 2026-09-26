from langchain.agents import create_agent

from app.ai.model import model
from app.tools.knowledge import search_knowledge_base
from app.tools.tickets import create_support_ticket
from app.memory.conversation import (
    get_messages,
    save_message,
)


agent = create_agent(
    model=model,
    tools=[
        search_knowledge_base,
        create_support_ticket,
    ],
    system_prompt="""
You are a customer support assistant.

For product-specific questions, use the knowledge base
tool to find information from the company's documentation.

Do not invent product-specific troubleshooting steps.

If the knowledge base does not contain enough information
to solve the customer's issue, create a support ticket
automatically.

If the customer says they already tried the recommended
troubleshooting and the issue is still unresolved,
create a support ticket automatically.

Do not wait for the customer to explicitly ask for a ticket
when the issue is clearly unresolved.

Only create a ticket when the customer's issue is genuinely
unresolved. Do not create tickets for normal informational
questions.

When you create a ticket, tell the customer the ticket ID.
""",
)


def ask_agent(
    conversation_id: int,
    question: str,
) -> str:

    save_message(
        conversation_id,
        "user",
        question,
    )

    history = get_messages(conversation_id)

    messages = [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in history
    ]

    response = agent.invoke(
        {
            "messages": messages
        }
    )

    answer = response["messages"][-1].text

    save_message(
        conversation_id,
        "assistant",
        answer,
    )

    return answer
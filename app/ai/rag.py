from app.ai.model import model
from src.retriever import search_knowledge


def answer_question(question: str) -> str:
    # 1. Search the knowledge base for relevant chunks
    results = search_knowledge(question, k=5)

    # 2. Convert the retrieved chunks into one piece of context
    context = "\n\n".join(
        result["content"]
        for result in results
    )

    # 3. Build the prompt that will be sent to Gemini
    prompt = f"""
You are a customer support assistant.

Answer the user's question using only the information
provided in the knowledge base context below.

If the context does not contain enough information to
answer the question, say that the available knowledge
base does not contain enough information.

Do not invent troubleshooting steps or facts.

Knowledge base context:
{context}

User question:
{question}

Answer:
"""

    # 4. Send the prompt to Gemini
    response = model.invoke(prompt)

    # 5. Return Gemini's generated text
    return response.text
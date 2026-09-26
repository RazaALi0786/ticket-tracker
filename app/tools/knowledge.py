from langchain_core.tools import tool

from src.retriever import search_knowledge


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the customer support knowledge base for relevant information.

    Use this tool when you need information from the company's
    documentation to answer a customer question.
    """

    results = search_knowledge(query, k=5)

    if not results:
        return "No relevant information was found in the knowledge base."

    context = "\n\n".join(
        result["content"]
        for result in results
    )

    return context
from app.tools.knowledge import search_knowledge_base


def main() -> None:
    query = "I cannot connect to the VPN. How can I fix this issue?"

    result = search_knowledge_base.invoke(
        {"query": query}
    )

    print("\nTool result:")
    print(result)


if __name__ == "__main__":
    main()
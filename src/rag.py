from retriever import search_knowledge
from generator import generate_answer

def build_context(results: list[dict]) -> str:

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
Chunk ID: {result['id']}

{result['content']}
"""
        )

    return "\n".join(context_parts)

def answer_question(
    question: str,
    k: int = 5,
) -> str:

    results = search_knowledge(
        question,
        k=k,
    )

    context = build_context(results)

    answer = generate_answer(
        question,
        context,
    )

    return answer


def main() -> None:

    question = "I cannot connect to the VPN. How can I fix this issue?"

    answer = answer_question(
        question,
        k=5,
    )

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)


if __name__ == "__main__":
    main()
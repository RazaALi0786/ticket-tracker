from app.ai.rag import answer_question


def main() -> None:
    question = "I cannot connect to the VPN. How can I fix this issue?"

    answer = answer_question(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()
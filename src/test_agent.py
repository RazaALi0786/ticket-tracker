from app.ai.agent import ask_agent
from app.memory.conversation import create_conversation


def main() -> None:
    conversation_id = create_conversation()

    print(f"Conversation ID: {conversation_id}")

    question_1 = "My VPN isn't connecting. What should I try?"

    answer_1 = ask_agent(
        conversation_id,
        question_1,
    )

    print("\nUser:")
    print(question_1)

    print("\nAgent:")
    print(answer_1)

    question_2 = "I tried that, but it still doesn't work."

    answer_2 = ask_agent(
        conversation_id,
        question_2,
    )

    print("\nUser:")
    print(question_2)

    print("\nAgent:")
    print(answer_2)


if __name__ == "__main__":
    main()
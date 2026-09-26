from app.memory.conversation import (
    create_conversation,
    get_messages,
    save_message,
)


def main() -> None:
    conversation_id = create_conversation()

    print(f"Created conversation: {conversation_id}")

    save_message(
        conversation_id,
        "user",
        "My VPN isn't working.",
    )

    save_message(
        conversation_id,
        "assistant",
        "Try enabling automatic retry.",
    )

    save_message(
        conversation_id,
        "user",
        "I tried that.",
    )

    messages = get_messages(conversation_id)

    print("\nConversation history:")

    for message in messages:
        print(f"{message['role']}: {message['content']}")


if __name__ == "__main__":
    main()
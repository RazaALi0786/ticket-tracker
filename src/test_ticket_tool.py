from app.tools.tickets import create_support_ticket


def main() -> None:
    result = create_support_ticket.invoke(
        {
            "title": "VPN connection problem",
            "description": "Customer is unable to connect to the VPN.",
            "customer_message": "My VPN still doesn't work. Please create a ticket.",
        }
    )

    print("\nTool result:")
    print(result)


if __name__ == "__main__":
    main()
from database import engine


def main() -> None:
    with engine.connect() as connection:
        result = connection.exec_driver_sql("SELECT version();")
        print(result.fetchone()[0])


if __name__ == "__main__":
    main()
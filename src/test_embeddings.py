from langchain_huggingface import HuggingFaceEmbeddings


def main() -> None:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    text = "My device won't turn on."

    vector = embeddings.embed_query(text)

    print(f"Vector dimensions: {len(vector)}")
    print(f"First 10 values: {vector[:10]}")


if __name__ == "__main__":
    main()
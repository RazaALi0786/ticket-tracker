from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy import text

from src.database import engine

def create_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def search_knowledge(
    query: str,
    k: int = 5,
) -> list[dict]:

    embeddings = create_embeddings()

    query_vector = embeddings.embed_query(query)

    sql = text(
        """
        SELECT
            id,
            content,
            metadata,
            embedding <=> CAST(:query_vector AS vector) AS distance
        FROM knowledge_chunks
        ORDER BY embedding <=> CAST(:query_vector AS vector)
        LIMIT :k
        """
    )

    with engine.connect() as connection:

        result = connection.execute(
            sql,
            {
                "query_vector": str(query_vector),
                "k": k,
            },
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def main() -> None:

    query = "I cannot connect to the VPN. How can I fix this issue?"

    results = search_knowledge(query, k=5)

    print(f"\nQuery: {query}")
    print(f"Retrieved {len(results)} chunks.\n")

    for result in results:

        print("=" * 60)

        print(f"Chunk ID: {result['id']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Content:\n{result['content']}")


if __name__ == "__main__":
    main()
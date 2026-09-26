from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy import text

from database import engine


PDF_PATH = Path("data/knowledge.pdf")


def load_pdf(pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    extracted_text = "\n".join(pages).strip()

    if not extracted_text:
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    return extracted_text


def split_text(content: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    return splitter.split_text(content)


def create_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def store_chunks(
    chunks: list[str],
    embeddings: HuggingFaceEmbeddings,
) -> None:

    vectors = embeddings.embed_documents(chunks)

    with engine.begin() as connection:

        for chunk, vector in zip(chunks, vectors):

            connection.execute(
                text(
                    """
                    INSERT INTO knowledge_chunks
                    (content, metadata, embedding)
                    VALUES (:content, CAST(:metadata AS JSONB), CAST(:embedding AS vector))
                    """
                ),
                {
                    "content": chunk,
                    "metadata": "{}",
                    "embedding": str(vector),
                },
            )


def main() -> None:

    print("Loading PDF...")

    content = load_pdf(PDF_PATH)

    print(f"Extracted {len(content)} characters.")

    print("Splitting text...")

    chunks = split_text(content)

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")

    embeddings = create_embeddings()

    print("Generating embeddings...")

    store_chunks(chunks, embeddings)

    print("Successfully stored chunks and embeddings.")


if __name__ == "__main__":
    main()
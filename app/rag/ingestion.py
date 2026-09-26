from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_PATH = Path("data/knowledge.pdf")


def load_pdf(pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    extracted_text = "\n".join(pages).strip()

    if not extracted_text:
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    return extracted_text


def split_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    return splitter.split_text(text)


def main() -> None:
    print(f"Loading PDF: {PDF_PATH}")

    text = load_pdf(PDF_PATH)

    print(f"Extracted {len(text)} characters.")

    chunks = split_text(text)

    print(f"Created {len(chunks)} chunks.")

    for index, chunk in enumerate(chunks):
        print(f"\n--- Chunk {index} ---")
        print(chunk)


if __name__ == "__main__":
    main()
from pathlib import Path
from src.pdf_preprocessor import process_pdfs_in_directory
from src.vector_store import create_vector_store


def main():
    BASE_DIR = Path(__file__).resolve().parent  # <-- change this
    docs_path = BASE_DIR / "SCHOLARSHIP_GUIDELINES"

    print(f"Looking for PDFs in: {docs_path}")

    chunks = process_pdfs_in_directory(docs_path)
    create_vector_store(chunks)

    print("\n Ingestion Completed Successfully!")


if __name__ == "__main__":
    main()
from pathlib import Path
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title


def process_pdfs_in_directory(directory_path="SCHOLARSHIP_GUIDELINES"):
    """
    Partition and chunk each PDF separately using title-based chunking.
    """

    directory_path = Path(directory_path)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    pdf_files = list(directory_path.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in directory.")

    print(f"📂 Found {len(pdf_files)} PDF files")

    all_chunks = []

    for file_path in pdf_files:
        print(f"\n📄 Processing: {file_path.name}")

        try:
            # 🔹 Step 1: Partition
            elements = partition_pdf(
                filename=str(file_path),
                strategy="hi_res",
                infer_table_structure=False,
                languages=["eng"],
            )

            print(f"   → Extracted {len(elements)} elements")

            # 🔹 Step 2: Chunk
            chunks = chunk_by_title(
                elements,
                max_characters=3000,
                new_after_n_chars=2400,
                combine_text_under_n_chars=500,
            )

            print(f"   → Created {len(chunks)} chunks")

            # 🔹 Step 3: Add filename metadata + prefix
            for chunk in chunks:
                chunk.metadata.source = file_path.name
                chunk.text = f"{file_path.name}\n\n{chunk.text}"

            # 🔹 Step 4: Store chunks
            all_chunks.extend(chunks)

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")

    print(f"\n🎉 Finished. Total chunks created: {len(all_chunks)}")

    return all_chunks

"""
if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent
    docs_path = BASE_DIR / "SCHOLARSHIP_GUIDELINES"

    all_chunks = process_pdfs_in_directory(docs_path)

    # 🔹 Print First 20 Chunks
    print("\n\n📌 Printing First 20 Chunks:\n")

    for i, chunk in enumerate(all_chunks[:20]):
        print("\n" + "=" * 100)
        print(f"Chunk {i+1}")
        print(f"Source: {getattr(chunk.metadata, 'source', 'Unknown')}")
        print(f"Length: {len(chunk.text)} characters")
        print("=" * 100)
        print(chunk.text[:500])  # print first 500 chars only
        print("...\n")
"""

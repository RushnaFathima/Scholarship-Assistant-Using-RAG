from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


def create_vector_store(chunks, per_dir="db/chroma_db"):

    print("🔹 Creating Embeddings Model")

    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    print("🔹 Converting chunks to LangChain Documents")

    langchain_docs = []

    for chunk in chunks:
        langchain_docs.append(
            Document(
                page_content=str(chunk.text),
                metadata={
                    "source": getattr(chunk.metadata, "source", "unknown")
                },
            )
        )

    print("🔹 Creating Vector Store")

    vector_store = Chroma.from_documents(
        documents=langchain_docs,
        embedding=embedding_model,
        persist_directory=per_dir,
        collection_metadata={"hnsw:space": "cosine"},
    )

    print(f"✅ Vector Store created and saved to {per_dir}")

    return vector_store
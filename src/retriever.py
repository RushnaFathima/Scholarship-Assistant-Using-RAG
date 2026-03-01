from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


PERSIST_DIRECTORY = "db/chroma_db"


def get_retriever():

    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model,
        collection_metadata={"hnsw:space": "cosine"},
    )

    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 5,
            "score_threshold": 0.3,
        },
    )

    return retriever
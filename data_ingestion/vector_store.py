from langchain_community.vectorstores import Chroma

def get_vector_store(embedding_model, persist_directory="./db_storage"):
    """Khởi tạo ChromaDB lưu trữ persistent trên disk."""
    return Chroma(
        collection_name="vn_legal_docs",
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )
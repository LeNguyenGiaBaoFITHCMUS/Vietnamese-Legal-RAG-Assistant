from data_ingestion.embedder import get_embedding_model
from langchain_community.vectorstores import Chroma

def get_retriever(persist_directory="./db_storage", k=4):
    # Khởi tạo Retriever từ ChromaDB hiện có
    embedder = get_embedding_model()
    
    db = Chroma(
        collection_name="vn_legal_docs",
        embedding_function=embedder,
        persist_directory=persist_directory
    )
    
    # Lấy ra 5 đoạn luật có liên quan nhất với câu hỏi
    return db.as_retriever(search_kwargs={"k": 3})
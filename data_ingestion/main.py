import logging
from loader import stream_legal_dataset
from parser import clean_html
from chunker import LegalChunker
from embedder import get_embedding_model
from vector_store import get_vector_store

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_ingestion_pipeline(batch_size=50, max_docs=None):
    logger.info("Khởi tạo các thành phần...")
    embedder = get_embedding_model() # Dùng model mặc định (BKAI)
    vector_store = get_vector_store(embedder)
    chunker = LegalChunker(chunk_size=1200, chunk_overlap=200)
    
    docs_processed = 0
    batch_documents = []
    
    for doc_id, html_content in stream_legal_dataset():
        if max_docs and docs_processed >= max_docs:
            break
            
        # 1. Parse HTML
        raw_text = clean_html(html_content)
        
        if not raw_text:
            continue
            
        # 2. Chunk theo ngữ cảnh pháp luật
        metadata = {"document_id": doc_id}
        chunks = chunker.split_document(raw_text, metadata)
        batch_documents.extend(chunks)
        
        docs_processed += 1
        
        # 3. Vectorize & Index theo batch
        if len(batch_documents) >= batch_size:
            logger.info(f"Đang index batch chứa {len(batch_documents)} chunks (Đã duyệt {docs_processed} docs)...")
            vector_store.add_documents(batch_documents)
            batch_documents = [] # Reset batch
            
    # Xử lý batch cuối cùng nếu còn sót lại
    if batch_documents:
        logger.info(f"Đang index batch cuối chứa {len(batch_documents)} chunks...")
        vector_store.add_documents(batch_documents)
        
    logger.info("Hoàn tất Data Ingestion!")

if __name__ == "__main__":
    # Tham số max_docs=100 dùng để test. Đặt thành None để chạy toàn bộ dữ liệu.
    run_ingestion_pipeline(batch_size=100, max_docs=None)
from data_ingestion.embedder import get_embedding_model
from data_ingestion.vector_store import get_vector_store

embedder = get_embedding_model()
db = get_vector_store(embedder)

# query = "Quy định về thời gian thử việc của người lao động"
query = "Công dân Việt Nam tham gia nghĩa vụ quân sự từ độ tuổi nào?"
# Tìm top 3 kết quả có độ tương đồng cao nhất
results = db.similarity_search_with_score(query, k=3)

print(f"Câu hỏi: {query}\n")
for idx, (doc, score) in enumerate(results):
    print(f"--- Top {idx + 1} | Khoảng cách: {score:.4f} ---")
    print(f"Metadata: {doc.metadata}")
    print(f"Trích đoạn: {doc.page_content[:200]}...\n")
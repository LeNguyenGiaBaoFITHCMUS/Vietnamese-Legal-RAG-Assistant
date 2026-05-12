from huggingface_hub import hf_hub_download
import pyarrow.parquet as pq
import logging

logger = logging.getLogger(__name__)

def stream_legal_dataset(repo_id="th1nhng0/vietnamese-legal-documents", filename="data/content.parquet"):
    """
    Đọc trực tiếp file Parquet theo từng Row Group.
    Bypass hoàn toàn thư viện 'datasets' để tránh lỗi tràn RAM (ArrowInvalid: large_string).
    """
    logger.info("Đang kiểm tra và tải file parquet trực tiếp từ HuggingFace Hub...")
    try:
        # Tải file parquet về cache máy tính (chỉ tải 1 lần duy nhất)
        file_path = hf_hub_download(repo_id=repo_id, filename=filename, repo_type="dataset")
        logger.info(f"Đã tìm thấy file tại cache: {file_path}")
        
        # Đọc parquet theo từng Row Group thay vì load toàn bộ file
        parquet_file = pq.ParquetFile(file_path)
        total_row_groups = parquet_file.num_row_groups
        
        for i in range(total_row_groups):
            # Đọc từng khối nhỏ (Row Group)
            table = parquet_file.read_row_group(i)
            
            # Chuyển trực tiếp sang Python List để bypass lỗi cast của Arrow
            doc_ids = table.column("id").to_pylist()
            htmls = table.column("content_html").to_pylist()
            
            # Yield từng dòng cho pipeline
            for doc_id, html_content in zip(doc_ids, htmls):
                # Bỏ qua các dòng bị null HTML (nếu có)
                if html_content is not None:
                    yield doc_id, html_content
                    
    except Exception as e:
        logger.error(f"Lỗi khi load dataset: {e}")
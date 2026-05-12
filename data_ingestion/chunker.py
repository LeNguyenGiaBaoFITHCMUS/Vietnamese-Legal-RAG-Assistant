import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class LegalChunker:
    def __init__(self, chunk_size=1000, chunk_overlap=150):
        # Fallback splitter cho các "Điều" quá dài
        self.fallback_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " "]
        )
        # Regex tìm pattern "Điều 1.", "Điều 1:", "ĐIỀU 1"
        self.dieu_pattern = re.compile(r'(?m)^(ĐIỀU|Điều)\s+(\d+[a-zA-Z]*)\s*[\.:]')

    def split_document(self, text: str, metadata: dict) -> list[Document]:
        chunks = []
        # Tách văn bản tại vị trí các "Điều"
        parts = self.dieu_pattern.split(text)
        
        if len(parts) == 1:
            # Không tìm thấy "Điều" nào, dùng chunking thông thường
            return self.fallback_splitter.create_documents([text], metadatas=[metadata])
        
        # Phần text trước "Điều 1" (thường là tiêu đề, căn cứ pháp lý)
        preamble = parts[0].strip()
        if preamble:
            preamble_docs = self.fallback_splitter.create_documents([preamble], metadatas=[{**metadata, "part": "preamble"}])
            chunks.extend(preamble_docs)

        # Iterate qua các "Điều" (parts chứa [..., "Điều", "1", "Nội dung...", ...])
        for i in range(1, len(parts), 3):
            prefix = parts[i]        # "Điều" hoặc "ĐIỀU"
            dieu_num = parts[i+1]    # "1", "2a"
            content = parts[i+2]     # Nội dung của điều
            
            full_dieu_text = f"{prefix} {dieu_num}. {content.strip()}"
            dieu_metadata = {
                **metadata,
                "dieu_so": dieu_num,
                "part": "dieu"
            }
            
            # Nếu nội dung điều kiện vượt quá giới hạn, cắt nhỏ tiếp
            if len(full_dieu_text) > self.fallback_splitter._chunk_size:
                sub_chunks = self.fallback_splitter.create_documents([full_dieu_text], metadatas=[dieu_metadata])
                chunks.extend(sub_chunks)
            else:
                chunks.append(Document(page_content=full_dieu_text, metadata=dieu_metadata))
                
        return chunks
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from rag_engine.retriever import get_retriever
from rag_engine.llm import get_llm

def build_rag_chain():
    retriever = get_retriever()
    llm = get_llm()

    # Prompt Engineering chống Hallucination (Bịa đặt)
    prompt_template = """Bạn là một chuyên gia tư vấn pháp luật Việt Nam.
    Hãy sử dụng CÁC TRÍCH ĐOẠN LUẬT sau đây để trả lời câu hỏi của người dùng. Luôn trình bày rõ ý và đảm bảo câu văn hoàn chỉnh.
    
    QUY TẮC NGHIÊM NGẶT:
    1. Nếu thông tin không có trong phần trích đoạn, hãy trả lời: "Dựa trên cơ sở dữ liệu hiện tại, tôi chưa tìm thấy quy định pháp luật cụ thể cho vấn đề này."
    2. KHÔNG tự bịa ra luật (hallucinate).
    3. Luôn trích dẫn "Điều X" hoặc "Mã văn bản" ở cuối câu trả lời dựa trên metadata cung cấp.

    TRÍCH ĐOẠN LUẬT:
    {context}

    CÂU HỎI: {question}

    CÂU TRẢ LỜI CỦA BẠN:"""

    prompt = PromptTemplate.from_template(prompt_template)

    # Hàm định dạng các chunks lấy từ DB để đưa vào Prompt
    def format_docs(docs):
        doc_strings = []
        for doc in docs:
            dieu_so = doc.metadata.get('dieu_so', '')
            doc_id = doc.metadata.get('document_id', '')
            prefix = f"[Văn bản số {doc_id} - Điều {dieu_so}]: " if dieu_so else f"[Văn bản số {doc_id}]: "
            doc_strings.append(prefix + doc.page_content)
        return "\n\n".join(doc_strings)

    # Khai báo Pipeline LCEL (LangChain Expression Language)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever
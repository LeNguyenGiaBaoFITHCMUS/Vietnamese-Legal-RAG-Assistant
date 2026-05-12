import streamlit as st
from rag_engine.chain import build_rag_chain

st.set_page_config(page_title="Trợ lý Pháp Luật AI", page_icon="⚖️", layout="centered")

st.title("⚖️ Trợ lý RAG Pháp Luật Việt Nam")
st.markdown("Xây dựng bởi LangChain, ChromaDB và Gemini AI")

# Tối ưu hóa: Chỉ khởi tạo chain 1 lần, lưu vào session_state
if "chain" not in st.session_state:
    st.session_state.chain, st.session_state.retriever = build_rag_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý input từ người dùng
if prompt := st.chat_input("Nhập câu hỏi pháp lý của bạn... (VD: Thời gian thử việc của người lao động là bao lâu?)"):
    # Hiện câu hỏi của người dùng
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Hiện câu trả lời của AI
    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu văn bản luật..."):
            # Lấy nguồn tài liệu trước để hiển thị
            docs = st.session_state.retriever.invoke(prompt)
            
            # Generator sinh câu trả lời
            response = st.session_state.chain.invoke(prompt)
            
            # Hiển thị text trả lời
            st.markdown(response)
            
            # Hiển thị Source Documents (Nguồn trích dẫn) dưới dạng Dropdown (Expander)
            with st.expander("Tài liệu tham khảo (Source Documents)"):
                for i, doc in enumerate(docs):
                    st.markdown(f"**Nguồn {i+1}: Văn bản {doc.metadata.get('document_id')}**")
                    st.info(doc.page_content[:500] + "...")
                    
    st.session_state.messages.append({"role": "assistant", "content": response})
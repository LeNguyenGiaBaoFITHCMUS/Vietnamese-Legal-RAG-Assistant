from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model(model_name="bkai-foundation-models/vietnamese-bi-encoder"):
    """Khởi tạo embedding model cho tiếng Việt."""
    model_kwargs = {'device': 'cpu'} # Chuyển thành 'cuda' nếu chạy trên máy có GPU
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
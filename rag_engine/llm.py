import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    # Khởi tạo mô hình Gemini 2.5 Flash từ Google
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.1, # Temperature thấp = AI trả lời nghiêm túc, bám sát facts, không bay bổng
        max_tokens=1024,
        # API key được tự động lấy từ file .env
    )
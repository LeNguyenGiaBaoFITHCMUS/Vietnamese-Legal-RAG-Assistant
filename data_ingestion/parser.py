from bs4 import BeautifulSoup
import re

def clean_html(html_content: str) -> str:
    """Loại bỏ noise từ HTML và trích xuất raw text."""
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Xóa script, style, meta
    for tag in soup(["script", "style", "meta", "noscript"]):
        tag.decompose()
        
    text = soup.get_text(separator="\n")
    
    # Chuẩn hóa khoảng trắng và dòng trống
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()
import re
import unicodedata

class TextPreprocessor:
    """Cleans and normalizes raw text for NLP processing."""
    def process(self, text: str) -> str:
        if not text:
            return ""
            
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode()
        text = text.lower()
        
        # Remove URLs and emails
        text = re.sub(r"http\S+", " ", text)
        text = re.sub(r"\S+@\S+", " ", text)
        
        # Keep alphanumeric, spaces, and specific tech symbols (+, #, .)
        text = re.sub(r"[^\w\s\+\#\.]", " ", text)
        text = re.sub(r"\s+", " ", text)
        
        return text.strip()

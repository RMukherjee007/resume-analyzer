import re
import unicodedata
from typing import List

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class TextPreprocessor:
    """
    Handles deterministic text preprocessing for resumes and job descriptions.
    """

    TECHNICAL_PATTERNS = [
        r'\bc\+\+\b',
        r'\bc#\b',
        r'\b\.net\b',
        r'\bios\b',
        r'\bjavascript\b',
        r'\btypescript\b',
        r'\bnode\.js\b'
    ]

    def __init__(self):
        # Stopwords are only applied during tokenization (optional)
        self.stopwords = set(stopwords.words("english"))
        self.stopwords -= {"with", "using", "in", "including"}

    def process(self, text: str) -> str:
        """
        Normalize and clean text while preserving technical terms.
        """
        if not text:
            return ""

        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")

        # Remove URLs, emails, phone numbers
        text = re.sub(r"http\S+|www\.\S+", " ", text)
        text = re.sub(r"\S+@\S+", " ", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", " ", text)

        text = text.lower()

        # Preserve special characters used in technical terms
        text = re.sub(r"[^\w\s\+\#\.\-]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        # Reinforce technical patterns with word boundaries
        for pattern in self.TECHNICAL_PATTERNS:
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            for match in matches:
                safe = match.lower()
                text = re.sub(
                    rf"\b{re.escape(safe)}\b",
                    safe,
                    text,
                    flags=re.IGNORECASE
                )

        return text

    def tokenize(self, text: str, remove_stopwords: bool = False) -> List[str]:
        """
        Tokenize text with optional stopword removal.
        """
        if not text:
            return []

        try:
            tokens = word_tokenize(text)
        except Exception:
            tokens = text.split()

        tokens = [t for t in tokens if len(t) >= 2]

        if remove_stopwords:
            tokens = [t for t in tokens if t not in self.stopwords]

        return tokens

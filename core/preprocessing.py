import re
import unicodedata


class TextPreprocessor:

    def process(self, text: str):

        if not text:
            return ""

        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode()

        text = text.lower()

        text = re.sub(r"http\S+", " ", text)
        text = re.sub(r"\S+@\S+", " ", text)

        text = re.sub(r"[^\w\s\+\#\.]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

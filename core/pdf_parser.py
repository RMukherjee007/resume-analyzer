from pathlib import Path
import pdfplumber


class PDFParser:

    def extract_text(self, pdf_path: Path):
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text_parts.append(content)
        return "\n".join(text_parts)

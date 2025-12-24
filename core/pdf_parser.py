from typing import List, Protocol, Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PDFExtractionStrategy(Protocol):
    """
    Protocol enforcing extraction interface for PDF strategies.
    """

    name: str

    def extract(self, pdf_path: Path) -> str:
        ...


class PDFParser:
    """
    Uses Strategy pattern to try different PDF extraction methods.
    Pattern justified: PDFs vary widely in structure and encoding.
    """

    def __init__(self, strategies: List[PDFExtractionStrategy] | None = None):
        self.strategies = strategies or [
            PDFPlumberStrategy(),
            PyPDF2Strategy()
        ]

    def extract_text(self, pdf_file: Union[str, Path]) -> str:
        """
        Attempts to extract text using multiple strategies.
        """
        pdf_path = self._normalize_input(pdf_file)
        errors: List[str] = []

        for strategy in self.strategies:
            try:
                text = strategy.extract(pdf_path)
                if self._is_valid(text):
                    logger.info(
                        "Extracted %d chars using %s",
                        len(text),
                        strategy.name
                    )
                    return text
            except Exception as exc:
                errors.append(f"{strategy.name}: {exc}")

        raise ValueError(
            "All PDF extraction strategies failed. "
            + " | ".join(errors)
        )

    @staticmethod
    def _normalize_input(pdf_file: Union[str, Path]) -> Path:
        """
        Normalize input to Path object.
        """
        if isinstance(pdf_file, Path):
            return pdf_file

        if isinstance(pdf_file, str):
            return Path(pdf_file)

        raise TypeError(
            f"Unsupported PDF input type: {type(pdf_file)}"
        )

    @staticmethod
    def _is_valid(text: str, min_length: int = 100) -> bool:
        """
        Heuristic validation to ensure extracted text is meaningful.
        """
        if not text:
            return False

        stripped = text.strip()
        if len(stripped) < min_length:
            return False

        total_chars = len(stripped)
        if total_chars == 0:
            return False

        alpha_chars = sum(c.isalpha() for c in stripped)
        alpha_ratio = alpha_chars / total_chars

        return alpha_ratio > 0.4

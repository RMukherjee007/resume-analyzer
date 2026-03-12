import numpy as np
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

@dataclass
class SimilarityResult:
    overall_score: float
    interpretation: str

class SimilarityEngine:
    """Calculates document similarity using a hybrid TF-IDF and Semantic approach."""
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=6000,
            stop_words="english",
            sublinear_tf=True,
            token_pattern=r"(?u)(?:\b|\s)([\w\+\#\.]+)(?:\b|\s)"
        )
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def compute_similarity(self, resume_text: str, jd_text: str) -> SimilarityResult:
        if not resume_text.strip() or not jd_text.strip():
             return SimilarityResult(0.0, "Empty text provided")

        docs = [resume_text, jd_text]

        try:
            tfidf = self.vectorizer.fit_transform(docs)
            tfidf_score = cosine_similarity(tfidf[0], tfidf[1])[0][0]
        except ValueError:
            tfidf_score = 0.0

        embeddings = self.embedder.encode(docs)
        semantic_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        # Weighted hybrid score (55% Semantic, 45% Keyword)
        final_score = 0.55 * semantic_score + 0.45 * tfidf_score

        return SimilarityResult(
            overall_score=float(final_score),
            interpretation=self._interpret(final_score)
        )

    def _interpret(self, score: float) -> str:
        if score >= 0.8: return "Strong match"
        if score >= 0.6: return "Good match"
        if score >= 0.45: return "Moderate match"
        return "Weak match"

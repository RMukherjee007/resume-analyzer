import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class SimilarityResult:
    """
    Result of resume–job description similarity analysis.
    """
    overall_score: float
    interpretation: str
    top_matching_terms: List[Tuple[str, float]]
    resume_unique_terms: List[str]
    jd_unique_terms: List[str]
    jaccard_similarity: float
    term_coverage: float


class SimilarityEngine:
    """
    Computes explainable similarity metrics using TF-IDF and cosine similarity.
    """

    def __init__(self):
        self._vectorizer_config = dict(
            ngram_range=(1, 3),
            max_features=5000,
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            stop_words="english",
            token_pattern=r"(?u)\b[\w\+\#\.]+\b",
        )

    def compute_similarity(self, resume_text: str, jd_text: str) -> SimilarityResult:
        if not resume_text or not jd_text:
            raise ValueError("Both resume and job description text are required")

        vectorizer = TfidfVectorizer(**self._vectorizer_config)
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])

        resume_vec, jd_vec = tfidf_matrix[0], tfidf_matrix[1]
        feature_names = np.array(vectorizer.get_feature_names_out())

        if resume_vec.nnz == 0 or jd_vec.nnz == 0:
            raise ValueError("Insufficient textual content for similarity analysis")

        score = float(cosine_similarity(resume_vec, jd_vec)[0][0])

        return SimilarityResult(
            overall_score=score,
            interpretation=self._interpret(score),
            top_matching_terms=self._top_matching_terms(
                resume_vec, jd_vec, feature_names
            ),
            resume_unique_terms=self._unique_terms(
                resume_vec, jd_vec, feature_names
            ),
            jd_unique_terms=self._unique_terms(
                jd_vec, resume_vec, feature_names
            ),
            jaccard_similarity=self._jaccard_overlap(resume_vec, jd_vec),
            term_coverage=self._jd_coverage(resume_vec, jd_vec),
        )

    @staticmethod
    def _top_matching_terms(resume_vec, jd_vec, features, n: int = 10):
        resume_scores = resume_vec.toarray().ravel()
        jd_scores = jd_vec.toarray().ravel()

        overlap = np.minimum(resume_scores, jd_scores)
        top_idx = overlap.argsort()[-n:][::-1]

        return [
            (features[i], float(overlap[i]))
            for i in top_idx
            if overlap[i] > 0
        ]

    @staticmethod
    def _unique_terms(doc_vec, other_vec, features, n: int = 10, threshold: float = 0.1):
        doc_scores = doc_vec.toarray().ravel()
        other_scores = other_vec.toarray().ravel()

        mask = (doc_scores > threshold) & (other_scores < threshold / 2)
        idx = np.where(mask)[0]

        if idx.size == 0:
            return []

        sorted_idx = idx[np.argsort(doc_scores[idx])[::-1]][:n]
        return features[sorted_idx].tolist()

    @staticmethod
    def _jaccard_overlap(vec1, vec2) -> float:
        """
        Vector-level Jaccard overlap of non-zero TF-IDF indices.
        """
        s1 = set(np.where(vec1.toarray().ravel() > 0)[0])
        s2 = set(np.where(vec2.toarray().ravel() > 0)[0])

        union = s1 | s2
        return len(s1 & s2) / len(union) if union else 0.0

    @staticmethod
    def _jd_coverage(resume_vec, jd_vec) -> float:
        """
        Fraction of JD terms covered by resume terms.
        """
        resume_terms = set(np.where(resume_vec.toarray().ravel() > 0)[0])
        jd_terms = set(np.where(jd_vec.toarray().ravel() > 0)[0])

        return len(resume_terms & jd_terms) / max(len(jd_terms), 1)

    @staticmethod
    def _interpret(score: float) -> str:
        if score >= 0.75:
            return "Strong match"
        if score >= 0.60:
            return "Good match"
        if score >= 0.45:
            return "Moderate match"
        if score >= 0.30:
            return "Weak match"
        return "Poor match"


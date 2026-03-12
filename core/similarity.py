from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SimilarityResult:
    overall_score: float
    interpretation: str
    top_matching_terms: List[Tuple[str, float]]
    jaccard_similarity: float
    term_coverage: float


class SimilarityEngine:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=6000,
            stop_words="english",
            sublinear_tf=True,
            token_pattern=r"(?u)\b[\w\+\#\.]+\b"
        )

        # semantic model
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def compute_similarity(self, resume_text, jd_text):

        docs = [resume_text, jd_text]

        tfidf = self.vectorizer.fit_transform(docs)

        resume_vec, jd_vec = tfidf[0], tfidf[1]

        tfidf_score = cosine_similarity(resume_vec, jd_vec)[0][0]

        embeddings = self.embedder.encode(docs)

        semantic_score = cosine_similarity(
            [embeddings[0]], [embeddings[1]]
        )[0][0]

        final_score = 0.55 * semantic_score + 0.45 * tfidf_score

        features = self.vectorizer.get_feature_names_out()

        return SimilarityResult(
            overall_score=float(final_score),
            interpretation=self._interpret(final_score),
            top_matching_terms=self._top_terms(resume_vec, jd_vec, features),
            jaccard_similarity=self._jaccard(resume_vec, jd_vec),
            term_coverage=self._coverage(resume_vec, jd_vec)
        )

    def _top_terms(self, r, j, features, n=10):

        r_arr = r.toarray().ravel()
        j_arr = j.toarray().ravel()

        overlap = np.minimum(r_arr, j_arr)

        idx = overlap.argsort()[-n:][::-1]

        return [(features[i], float(overlap[i])) for i in idx if overlap[i] > 0]

    def _jaccard(self, v1, v2):

        s1 = set(np.where(v1.toarray().ravel() > 0)[0])
        s2 = set(np.where(v2.toarray().ravel() > 0)[0])

        union = s1 | s2

        return len(s1 & s2) / len(union) if union else 0

    def _coverage(self, resume_vec, jd_vec):

        r = set(np.where(resume_vec.toarray().ravel() > 0)[0])
        j = set(np.where(jd_vec.toarray().ravel() > 0)[0])

        return len(r & j) / max(len(j), 1)

    def _interpret(self, score):

        if score >= 0.8:
            return "Strong match"
        if score >= 0.6:
            return "Good match"
        if score >= 0.45:
            return "Moderate match"
        return "Weak match"

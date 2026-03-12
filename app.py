import streamlit as st
from pathlib import Path
import tempfile

from core import (
    PDFParser,
    TextPreprocessor,
    SimilarityEngine,
    SkillExtractor,
    GapAnalyzer
)


st.set_page_config(page_title="Resume Analyzer", layout="wide")

parser = PDFParser()
preprocessor = TextPreprocessor()
similarity_engine = SimilarityEngine()
skill_extractor = SkillExtractor()
gap_analyzer = GapAnalyzer()


st.title("AI Resume Analyzer")

uploaded = st.file_uploader("Upload Resume", type=["pdf"])
jd = st.text_area("Paste Job Description")


if st.button("Analyze"):

    with tempfile.NamedTemporaryFile(delete=False) as tmp:

        tmp.write(uploaded.read())
        pdf_path = Path(tmp.name)

    resume_text = parser.extract_text(pdf_path)

    resume_text = preprocessor.process(resume_text)
    jd = preprocessor.process(jd)

    resume_skills = skill_extractor.extract_skills(resume_text)
    jd_skills = skill_extractor.extract_skills(jd)

    similarity = similarity_engine.compute_similarity(resume_text, jd)

    report = gap_analyzer.analyze(resume_skills, jd_skills)

    fit_score = (
        0.55 * similarity.overall_score
        + 0.30 * report.coverage
        + 0.15 * (report.matched / max(len(jd_skills), 1))
    )

    st.metric("Match Score", f"{similarity.overall_score:.2f}")
    st.metric("Skill Coverage", f"{report.coverage:.2f}")
    st.metric("Candidate Fit Score", f"{fit_score:.2f}")

    st.write(similarity.interpretation)

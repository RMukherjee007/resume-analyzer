import streamlit as st
from pathlib import Path
import tempfile
import os

from core import (
    PDFParser,
    TextPreprocessor,
    SimilarityEngine,
    SkillExtractor,
    GapAnalyzer
)

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Cache heavy machine learning models so they don't reload on every interaction
@st.cache_resource
def load_engines():
    return SimilarityEngine(), SkillExtractor()

similarity_engine, skill_extractor = load_engines()

# Instantiate lightweight classes normally
parser = PDFParser()
preprocessor = TextPreprocessor()
gap_analyzer = GapAnalyzer()

st.title("AI Resume Analyzer")

uploaded = st.file_uploader("Upload Resume", type=["pdf"])
jd = st.text_area("Paste Job Description")

if st.button("Analyze"):
    
    # 1. Check for valid inputs before proceeding
    if not uploaded:
        st.error("Please upload a resume (PDF).")
    elif not jd.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analyzing resume..."):
            pdf_path = None
            try:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded.read())
                    pdf_path = Path(tmp.name)

                # Extract and clean text
                resume_text = parser.extract_text(pdf_path)
                resume_text = preprocessor.process(resume_text)
                jd_clean = preprocessor.process(jd)

                if not resume_text.strip():
                    st.error("Could not extract any readable text from the PDF.")
                else:
                    # Extract skills
                    resume_skills = skill_extractor.extract_skills(resume_text)
                    jd_skills = skill_extractor.extract_skills(jd_clean)

                    # Compute metrics
                    similarity = similarity_engine.compute_similarity(resume_text, jd_clean)
                    report = gap_analyzer.analyze(resume_skills, jd_skills)

                    jd_skill_count = max(len(jd_skills), 1)
                    skill_match_ratio = report.matched / jd_skill_count

                    fit_score = (
                        0.55 * similarity.overall_score
                        + 0.30 * report.coverage
                        + 0.15 * skill_match_ratio
                    )

                    breakdown = {
                        "similarity_score": round(similarity.overall_score, 4),
                        "skill_coverage": round(report.coverage, 4),
                        "skill_match_ratio": round(skill_match_ratio, 4),
                        "final_fit_score": round(fit_score, 4),
                    }

                    # Display UI
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Match Score", f"{similarity.overall_score:.2f}")
                    col2.metric("Skill Coverage", f"{report.coverage:.2f}")
                    col3.metric("Candidate Fit Score", f"{fit_score:.2f}")

                    st.subheader("Score Breakdown")
                    st.json(breakdown)

                    st.write(similarity.interpretation)

            finally:
                # 2. Cleanup to prevent local storage leaks
                if pdf_path and pdf_path.exists():
                    os.remove(pdf_path)

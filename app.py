import streamlit as st
import os
import tempfile
from pathlib import Path

from core import (
    PDFParser,
    TextPreprocessor,
    SimilarityEngine,
    SkillExtractor,
    GapAnalyzer
)

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Cache heavy machine learning models
@st.cache_resource
def load_engines():
    return SimilarityEngine(), SkillExtractor()

similarity_engine, skill_extractor = load_engines()
parser = PDFParser()
preprocessor = TextPreprocessor()
gap_analyzer = GapAnalyzer()

st.title("AI Resume Analyzer 🚀")

uploaded = st.file_uploader("Upload Resume", type=["pdf"])
jd = st.text_area("Paste Job Description", height=200)

if st.button("Analyze Candidate", type="primary"):
    if not uploaded or not jd.strip():
        st.error("Please provide both a PDF resume and a Job Description.")
    else:
        with st.spinner("Processing documents..."):
            pdf_path = None
            try:
                # Securely handle file upload
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded.read())
                    pdf_path = Path(tmp.name)

                # Parsing and Preprocessing
                resume_text = preprocessor.process(parser.extract_text(pdf_path))
                jd_clean = preprocessor.process(jd)

                if not resume_text.strip():
                    st.error("Could not extract readable text from the PDF.")
                else:
                    # Extraction and Scoring
                    resume_skills = skill_extractor.extract_skills(resume_text)
                    jd_skills = skill_extractor.extract_skills(jd_clean)
                    
                    similarity = similarity_engine.compute_similarity(resume_text, jd_clean)
                    report = gap_analyzer.analyze(resume_skills, jd_skills)

                    # Final Fit Score Calculation
                    fit_score = (0.60 * similarity.overall_score) + (0.40 * report.coverage)

                    # Metrics Display
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Candidate Fit Score", f"{fit_score:.2f}")
                    col2.metric("Semantic Match", f"{similarity.overall_score:.2f}")
                    col3.metric("Skill Coverage", f"{report.coverage:.2f}")
                    
                    st.write(f"**Engine Interpretation:** {similarity.interpretation}")
                    st.divider()

                    # Gap Analysis Display
                    st.subheader("Skill Gap Analysis")
                    if report.missing_skills:
                        st.warning(f"**Missing Skills:** {', '.join(report.missing_skills)}")
                    elif jd_skills:
                        st.success("Candidate matches all extracted JD skills!")
                    else:
                        st.info("No specific technical skills identified in the Job Description.")

            finally:
                # Ensure temporary file is always deleted
                if pdf_path and pdf_path.exists():
                    os.remove(pdf_path)

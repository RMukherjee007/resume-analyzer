import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import tempfile
import os

# Assume core files are properly imported here 
from core.pdf_parser import PDFParser
from core.preprocessing import TextPreprocessor
from core.similarity import SimilarityEngine
from core.skills import SkillExtractor

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

@st.cache_resource
def load_engines():
    return SimilarityEngine(), SkillExtractor()

similarity_engine, skill_extractor = load_engines()
parser = PDFParser()
preprocessor = TextPreprocessor()

st.title("AI Resume Analyzer")

uploaded = st.file_uploader("Upload Resume", type=["pdf"])
jd = st.text_area("Paste Job Description", height=200)

if st.button("Analyze Candidate", type="primary"):
    if not uploaded or not jd.strip():
        st.error("Please provide both a PDF resume and a Job Description.")
    else:
        with st.spinner("Processing documents..."):
            pdf_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded.read())
                    pdf_path = Path(tmp.name)

                resume_text = preprocessor.process(parser.extract_text(pdf_path))
                jd_clean = preprocessor.process(jd)

                resume_skills = skill_extractor.extract_skills(resume_text)
                jd_skills = skill_extractor.extract_skills(jd_clean)
                similarity = similarity_engine.compute_similarity(resume_text, jd_clean)

                # Gap Analysis Logic
                resume_skill_names = {s.skill.name for s in resume_skills}
                jd_skill_names = {s.skill.name for s in jd_skills}
                matched_count = len(resume_skill_names & jd_skill_names)
                
                skill_coverage = matched_count / max(len(jd_skill_names), 1)
                fit_score = (0.60 * similarity.overall_score) + (0.40 * skill_coverage)

                # UI Display
                col1, col2, col3 = st.columns(3)
                col1.metric("Candidate Fit Score", f"{fit_score:.2f}")
                col2.metric("Semantic Match", f"{similarity.overall_score:.2f}")
                col3.metric("Skill Coverage", f"{skill_coverage:.2f}")
                
                missing_skills = [name.title() for name in jd_skill_names if name not in resume_skill_names]
                if missing_skills:
                    st.warning(f"**Missing Skills:** {', '.join(missing_skills)}")
                else:
                    st.success("Candidate matches all extracted JD skills.")

            finally:
                if pdf_path and pdf_path.exists():
                    os.remove(pdf_path)

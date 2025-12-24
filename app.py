import streamlit as st
import sys
from pathlib import Path
import tempfile

sys.path.insert(0, str(Path(__file__).parent))

from core.pdf_parser import PDFParser
from core.preprocessing import TextPreprocessor
from core.similarity import SimilarityEngine
from core.skills import SkillExtractor
from core.gap_analysis import GapAnalyzer

st.set_page_config(page_title="Resume Analyzer", page_icon="🎯", layout="wide")

st.markdown("""
<style>
.main-header {font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center;}
.skill-match {background-color: #d4edda; padding: 0.5rem; border-radius: 0.3rem; margin: 0.3rem 0;}
.skill-missing {background-color: #f8d7da; padding: 0.5rem; border-radius: 0.3rem; margin: 0.3rem 0;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_components():
    """Initialize components once."""
    return (
        PDFParser(),
        TextPreprocessor(),
        SimilarityEngine(),
        SkillExtractor(),
        GapAnalyzer()
    )

def analyze_resume(pdf_file, jd_text, components):
    parser, preprocessor, sim_engine, skill_extractor, gap_analyzer = components

    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        pdf_path = Path(tmp.name)

    with st.spinner("Extracting PDF..."):
        resume_text = parser.extract_text(pdf_path)

    if not resume_text or len(resume_text.strip()) < 100:
        raise ValueError("Resume text too short or unreadable")

    with st.spinner("Preprocessing..."):
        clean_resume = preprocessor.process(resume_text)
        clean_jd = preprocessor.process(jd_text)

    with st.spinner("Computing similarity..."):
        similarity = sim_engine.compute_similarity(clean_resume, clean_jd)

    with st.spinner("Analyzing skills..."):
        resume_skills = skill_extractor.extract_skills(clean_resume)
        jd_skills = skill_extractor.extract_skills(clean_jd)

    with st.spinner("Analyzing gaps..."):
        gap_report = gap_analyzer.analyze(resume_skills, jd_skills)

    return similarity, gap_report

def render_similarity(sim):
    st.markdown("#### Similarity Analysis")
    st.info(f"**{sim.interpretation}** ({sim.overall_score:.1%})")
    st.progress(sim.overall_score)

    st.markdown("##### Top Matching Terms")
    for term, score in sim.top_matching_terms:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{term}**")
        with col2:
            st.caption(f"{score:.3f}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Term Coverage", f"{sim.term_coverage:.1%}")
    with col2:
        st.metric("Jaccard", f"{sim.jaccard_similarity:.1%}")

def render_matched(matched):
    st.markdown(f"#### ✅ Matched Skills ({len(matched)})")
    if not matched:
        st.info("No matched skills")
        return

    by_cat = {}
    for match in matched:
        by_cat.setdefault(match.skill.category, []).append(match)

    for cat, skills in by_cat.items():
        with st.expander(f"{cat.value.title()} ({len(skills)})", expanded=True):
            for match in skills:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f'<div class="skill-match">✅ {match.skill.name}</div>',
                        unsafe_allow_html=True
                    )
                with col2:
                    st.caption(f"{match.confidence:.0%}")

def render_missing(missing, cat_analysis):
    st.markdown(f"#### ❌ Missing Skills ({len(missing)})")
    if not missing:
        st.success("All skills present!")
        return

    by_priority = {}
    for gap in missing:
        by_priority.setdefault(gap.priority.value, []).append(gap)

    emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
    for priority in ["Critical", "High", "Medium", "Low"]:
        if priority in by_priority:
            with st.expander(
                f"{emoji[priority]} {priority} ({len(by_priority[priority])})",
                expanded=priority in ["Critical", "High"]
            ):
                for gap in by_priority[priority]:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(
                            f'<div class="skill-missing">❌ {gap.skill_name}</div>',
                            unsafe_allow_html=True
                        )
                    with col2:
                        st.caption(f"{gap.impact_score:.0%}")

    if cat_analysis:
        import pandas as pd
        df = pd.DataFrame([
            {"Category": a.category.value.title(), "Coverage": a.coverage * 100}
            for a in cat_analysis.values()
        ])
        st.bar_chart(df.set_index("Category"))

def render_categories(cat_analysis):
    st.markdown("#### 📊 Category Analysis")
    for analysis in cat_analysis.values():
        color = "🟢" if analysis.coverage >= 0.75 else "🔴" if analysis.coverage < 0.5 else "🟡"
        with st.expander(
            f"{color} {analysis.category.value.title()}: {analysis.coverage:.0%}",
            expanded=analysis.coverage < 0.5
        ):
            col1, col2, col3 = st.columns(3)
            col1.metric("Strong", analysis.matched_count)
            col2.metric("Weak", analysis.weak_count)
            col3.metric("Missing", analysis.missing_count)

def render_recommendations(recs, gap_report):
    st.markdown("#### 💡 Recommendations")
    for i, rec in enumerate(recs, 1):
        with st.expander(f"{rec.priority} - {rec.title}", expanded=i <= 2):
            st.markdown(f"**{rec.description}**")
            st.markdown(f"➡️ {rec.action}")

    st.markdown("---")
    score, conf = gap_report.overall_score, gap_report.confidence_score

    if score >= 0.75 and conf >= 0.85:
        st.success("Strong overall match")
    elif score >= 0.6:
        st.info("Good overall match")
    else:
        st.warning("Needs improvement")

    col1, col2 = st.columns(2)
    col1.metric("Coverage", f"{score:.0%}")
    col2.metric("Confidence", f"{conf:.0%}")

def main():
    st.markdown('<div class="main-header">🎯 Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Clean OOP Architecture</p>", unsafe_allow_html=True)

    components = get_components()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Resume")
        uploaded = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded:
            st.success(uploaded.name)

    with col2:
        st.subheader("💼 Job Description")
        jd_text = st.text_area("Paste JD", height=200)

    st.markdown("---")
    if st.button("🚀 Analyze", type="primary", use_container_width=True):
        if not uploaded or not jd_text or len(jd_text.strip()) < 50:
            st.error("Please provide both resume and job description")
            return

        try:
            similarity, gap_report = analyze_resume(uploaded, jd_text, components)

            st.markdown("### 📊 Results")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Match", f"{similarity.overall_score:.0%}")
            col2.metric("Matched", len(gap_report.matched_skills))
            col3.metric("Missing", len(gap_report.missing_skills))
            col4.metric("Confidence", f"{gap_report.confidence_score:.0%}")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["📈 Similarity", "✅ Matched", "❌ Missing", "📊 Categories", "💡 Tips"]
            )

            with tab1: render_similarity(similarity)
            with tab2: render_matched(gap_report.matched_skills)
            with tab3: render_missing(gap_report.missing_skills, gap_report.category_analysis)
            with tab4: render_categories(gap_report.category_analysis)
            with tab5: render_recommendations(gap_report.recommendations, gap_report)

        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()

"""
app.py
AI Skill-Gap Career Navigator — Streamlit UI
Run with: streamlit run app.py
"""
 
import streamlit as st
import pandas as pd
 
from resume_parser import extract_resume_text
from gemini_helper import analyze_skill_gap
 
st.set_page_config(
    page_title="AI Skill-Gap Career Navigator",
    page_icon="🎯",
    layout="wide",
)
 
# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f7f8fc 0%, #ffffff 100%);
    }
    .hero {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        padding: 2.5rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.25);
    }
    .hero h1 { color: white !important; font-size: 2.4rem; margin-bottom: 0.4rem; }
    .hero p { color: rgba(255,255,255,0.9); font-size: 1.05rem; margin: 0; }
 
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #eef0f7;
        margin-bottom: 1.5rem;
        height: 100%;
    }
    .step-badge {
        display: inline-flex; align-items: center; justify-content: center;
        width: 28px; height: 28px; border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white; font-weight: 700; font-size: 0.9rem; margin-right: 0.5rem;
    }
 
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white; border: none; border-radius: 12px;
        padding: 0.85rem 1.5rem; font-size: 1.05rem; font-weight: 600;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.45);
        color: white;
    }
 
    .result-card {
        border-radius: 16px; padding: 1.25rem 1.5rem; height: 100%;
        border: 1px solid #eef0f7; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .card-matched { background: #f0fdf4; border-left: 5px solid #22c55e; }
    .card-must { background: #fef2f2; border-left: 5px solid #ef4444; }
    .card-good { background: #fffbeb; border-left: 5px solid #f59e0b; }
    .result-card h4 { margin-top: 0; }
    .result-card ul { padding-left: 1.1rem; margin-bottom: 0; }
    .result-card li { margin-bottom: 0.35rem; }
 
    .summary-box {
        background: #eef2ff; border-left: 5px solid #6366f1; border-radius: 12px;
        padding: 1.1rem 1.4rem; margin-bottom: 1.5rem; font-size: 1.02rem; line-height: 1.5;
    }
 
    .week-card {
        background: white; border-radius: 14px; border: 1px solid #eef0f7;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); padding: 1.1rem 1.4rem; margin-bottom: 1rem;
    }
    .week-title { font-weight: 700; font-size: 1.1rem; color: #4338ca; margin-bottom: 0.5rem; }
 
    .topic-pill {
        display: inline-block; background: #f3f0ff; color: #6d28d9;
        border-radius: 999px; padding: 0.4rem 0.9rem;
        margin: 0.25rem 0.35rem 0.25rem 0; font-size: 0.9rem; font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)
 
# ---------- HERO HEADER ----------
st.markdown("""
<div class="hero">
    <h1>🎯 AI Skill-Gap Career Navigator</h1>
    <p>Find exactly what's missing between your current skills and your target job —
    then get a week-by-week AI-generated roadmap to close the gap.</p>
</div>
""", unsafe_allow_html=True)
 
# ---------- INPUT SECTION ----------
col1, col2 = st.columns(2)
 
with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-badge">1</span> **Your Current Skills**', unsafe_allow_html=True)
    st.write("")
 
    input_method = st.radio(
        "How do you want to provide your skills?",
        ["Type them in", "Upload resume (PDF/DOCX/TXT)"],
        horizontal=True,
    )
 
    current_skills_text = ""
 
    if input_method == "Type them in":
        current_skills_text = st.text_area(
            "List your skills, tools, projects, experience (comma or line separated)",
            height=180,
            placeholder="e.g. Python, SQL, basic HTML/CSS, DSA (arrays, "
            "linked lists), one Flask project, Git basics...",
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload your resume", type=["pdf", "docx", "txt"]
        )
        if uploaded_file is not None:
            try:
                with st.spinner("Extracting text from resume..."):
                    current_skills_text = extract_resume_text(uploaded_file)
                st.success(f"Extracted {len(current_skills_text)} characters from resume.")
                with st.expander("Preview extracted text"):
                    st.text(current_skills_text[:2000])
            except Exception as e:
                st.error(f"Couldn't read that file: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
 
with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-badge">2</span> **Target Job Role**', unsafe_allow_html=True)
    st.write("")
 
    target_role = st.text_input(
        "Enter the exact role you're targeting",
        placeholder="e.g. Software Engineer at TCS, Backend Developer, Data Analyst",
    )
 
    roadmap_weeks = st.slider(
        "Roadmap length (weeks)",
        min_value=1,
        max_value=8,
        value=4,
        help="Use 1-2 weeks if your interview is very soon (last-mile prep). "
        "Use 4-8 weeks for a full skill-building plan.",
    )
    st.markdown('</div>', unsafe_allow_html=True)
 
st.write("")
analyze_clicked = st.button("🔍  Analyze Skill Gap", type="primary", use_container_width=True)
 
# ---------- ANALYSIS ----------
if analyze_clicked:
    if not current_skills_text.strip():
        st.warning("Please enter your skills or upload a resume first.")
    elif not target_role.strip():
        st.warning("Please enter a target job role.")
    else:
        try:
            with st.spinner("Asking Gemini to analyze your skill gap... this takes a few seconds"):
                result = analyze_skill_gap(current_skills_text, target_role, roadmap_weeks)
            st.session_state["result"] = result
        except Exception as e:
            st.error(f"Something went wrong calling Gemini: {e}")
 
# ---------- RESULTS ----------
if "result" in st.session_state:
    result = st.session_state["result"]
 
    st.write("")
    st.markdown("---")
    st.markdown(f"## 📋 Results for: *{result.get('target_role', target_role)}*")
 
    st.markdown(
        f'<div class="summary-box">{result.get("summary", "")}</div>',
        unsafe_allow_html=True,
    )
 
    col_a, col_b, col_c = st.columns(3)
 
    with col_a:
        matched = result.get("matched_skills", [])
        items_html = "".join(f"<li>{s}</li>" for s in matched) or "<li>None detected.</li>"
        st.markdown(f"""
        <div class="result-card card-matched">
            <h4>✅ Skills You Already Have</h4>
            <ul>{items_html}</ul>
        </div>
        """, unsafe_allow_html=True)
 
    with col_b:
        missing_must = result.get("missing_must_have", [])
        items_html = "".join(f"<li><b>{s}</b></li>" for s in missing_must) or "<li>None — you're covered!</li>"
        st.markdown(f"""
        <div class="result-card card-must">
            <h4>🔴 Missing — Must Have</h4>
            <ul>{items_html}</ul>
        </div>
        """, unsafe_allow_html=True)
 
    with col_c:
        missing_good = result.get("missing_good_to_have", [])
        items_html = "".join(f"<li>{s}</li>" for s in missing_good) or "<li>None.</li>"
        st.markdown(f"""
        <div class="result-card card-good">
            <h4>🟡 Missing — Good to Have</h4>
            <ul>{items_html}</ul>
        </div>
        """, unsafe_allow_html=True)
 
    st.write("")
    st.write("")
 
    # ---------- ROADMAP ----------
    st.markdown("### 🗺️ Week-by-Week Learning Roadmap")
    roadmap = result.get("roadmap", [])
 
    if roadmap:
        for week in roadmap:
            tasks_html = "".join(f"<li>{t}</li>" for t in week.get("tasks", []))
            resources_html = "".join(f"<li>{r}</li>" for r in week.get("resources", []))
            st.markdown(f"""
            <div class="week-card">
                <div class="week-title">Week {week.get('week')}: {week.get('focus', '')}</div>
                <b>Tasks:</b>
                <ul>{tasks_html}</ul>
                <b>Resources:</b>
                <ul>{resources_html}</ul>
            </div>
            """, unsafe_allow_html=True)
 
        rows = []
        for week in roadmap:
            rows.append({
                "Week": week.get("week"),
                "Focus": week.get("focus"),
                "Tasks": "; ".join(week.get("tasks", [])),
                "Resources": "; ".join(week.get("resources", [])),
            })
        df = pd.DataFrame(rows)
        st.download_button(
            "⬇️ Download roadmap as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="skill_gap_roadmap.csv",
            mime="text/csv",
        )
    else:
        st.write("No roadmap generated.")
 
    st.write("")
 
    # ---------- INTERVIEW PREP ----------
    st.markdown("### 🎤 Likely Interview Topics to Prep")
    topics = result.get("likely_interview_topics", [])
    pills_html = "".join(f'<span class="topic-pill">{t}</span>' for t in topics)
    st.markdown(f'<div>{pills_html}</div>', unsafe_allow_html=True)
 
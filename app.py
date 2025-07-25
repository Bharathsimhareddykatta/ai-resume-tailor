import time
import streamlit as st
import plotly.graph_objects as go
from core.resume_parser import parse_resume
from core.matching_engine import compare_keywords
from core.openrouter_engine import generate_resume_summary
from core.docx_exporter import generate_docx

# ---------- Page Config ----------
st.set_page_config(page_title="AI Resume Tailor", layout="centered")

# ---------- Sidebar ----------
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

# ---------- Dark Mode Styling ----------
if theme == "Dark":
    st.markdown("""
        <style>
        .main, .block-container {
            background-color: #0e1117 !important;
            color: #FAFAFA !important;
        }
        .stTextInput > div > input,
        .stTextArea textarea {
            background-color: #1c1f26 !important;
            color: #ffffff !important;
        }
        .stButton > button {
            background-color: #4CAF50 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ---------- Sidebar Instructions ----------
st.sidebar.title("🧭 How to Use")
st.sidebar.markdown("""
1. 📎 Upload Resume  
2. 📝 Paste Job Description  
3. ✨ Click 'Tailor Resume'  
4. ✅ View Summary, Skills, Score  
5. 📥 Download Report  
""")
st.sidebar.markdown("🔗 [GitHub](https://github.com/Bharathsimhareddykatta/ai-resume-tailor)")

# ---------- Header ----------
st.markdown("""
    <div style='background: linear-gradient(to right, #6a11cb, #2575fc); padding: 8px 8px; border-radius: 8px; text-align: center; color: white;'>
        <h2 style='margin-bottom: 5px;'>📄 AI Resume Tailor</h2>
        <p style='font-size: 14px;'>Tailor your resume to job descriptions using AI</p>
    </div>
""", unsafe_allow_html=True)

# ---------- Resume Upload Form ----------
with st.form("resume_form"):
    st.subheader("📎 Upload Resume & Paste JD")
    resume_file = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
    job_description = st.text_area("📝 Paste the job description", height=180)
    submitted = st.form_submit_button("✨ Tailor Resume")

# ---------- Keyword Chips ----------
def display_keywords(title, keywords, color):
    st.markdown(f"<h5 style='color:{color}'>{title}</h5>", unsafe_allow_html=True)
    if not keywords:
        st.success("✅ All good! No missing keywords.")
    else:
        chip_style = f"""
            display: inline-block;
            background-color: {color};
            color: white;
            padding: 6px 12px;
            margin: 4px;
            border-radius: 20px;
            font-size: 13px;
        """
        chips = " ".join([f"<span style='{chip_style}'>{kw}</span>" for kw in sorted(keywords)])
        st.markdown(chips, unsafe_allow_html=True)

# ---------- On Submit ----------
if submitted:
    if not resume_file:
        st.warning("📎 Please upload your resume.")
    elif not job_description.strip():
        st.warning("📝 Please paste the job description.")
    else:
        with st.spinner("📂 Parsing resume and comparing with job..."):
            progress_bar = st.progress(0, text="Processing...")
            for i in range(0, 101, 10):
                time.sleep(0.03)
                progress_bar.progress(i, text="Processing...")

            resume_text = parse_resume(resume_file)
            matched, missing = compare_keywords(resume_text, job_description)

        st.success("✅ Resume parsed and compared!")

        # ---------- Match Score ----------
        total_keywords = len(set(matched + missing))
        match_score = round((len(matched) / total_keywords) * 100) if total_keywords > 0 else 0

        st.markdown("### 📊 Resume Match Score")

        # Animated percentage counter
        score_placeholder = st.empty()
        for i in range(0, match_score + 1, 5):
            time.sleep(0.02)
            score_placeholder.markdown(f"<h2 style='text-align:center; color:#4CAF50;'>{i}%</h2>", unsafe_allow_html=True)

        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=match_score,
            title={'text': "Match %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#27ae60"},
                'steps': [
                    {'range': [0, 40], 'color': "#e74c3c"},
                    {'range': [40, 70], 'color': "#f39c12"},
                    {'range': [70, 100], 'color': "#2ecc71"}
                ]
            }
        ))
        fig.update_layout(
            height=250,
            paper_bgcolor="#0e1117" if theme == "Dark" else "white",
            font=dict(color="white" if theme == "Dark" else "black"),
            margin=dict(t=10, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)

        # ---------- Display Keywords ----------
        display_keywords("✅ Matched Keywords", matched, "#2ecc71")
        display_keywords("❌ Missing Keywords", missing, "#e74c3c")

        # ---------- AI Summary ----------
        with st.spinner("🤖 Generating AI Summary and Skills..."):
            try:
                response = generate_resume_summary(resume_text, job_description)

                if "### Skills Section:" in response:
                    summary, skills_raw = response.split("### Skills Section:")
                else:
                    summary = response
                    skills_raw = ""

                skills = [line.strip("- ").strip() for line in skills_raw.strip().split("\n") if line.strip()]

                with st.expander("🧠 Tailored Summary", expanded=True):
                    st.info(summary)

                with st.expander("💼 Suggested Skills", expanded=True):
                    if skills:
                        st.success("✔️ " + ", ".join(skills))
                    else:
                        st.warning("⚠️ No skills detected.")

                # ---------- Export .txt ----------
                report = f"AI Resume Tailor Report\n\n📊 Match Score: {match_score}%\n"
                report += "\n✅ Matched:\n" + (", ".join(matched) if matched else "None")
                report += "\n\n❌ Missing:\n" + (", ".join(missing) if missing else "None")
                report += "\n\n🧠 Summary:\n" + summary
                report += "\n\n💼 Skills:\n" + (", ".join(skills) if skills else "None")

                st.download_button("⬇️ Download Report (.txt)", report, "resume_tailor_report.txt", "text/plain")

                # ---------- Export .docx ----------
                docx_file = generate_docx(summary, skills, matched, missing)
                st.download_button("⬇️ Download Resume Report (.docx)", docx_file,
                                   "resume_tailor_report.docx",
                                   "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            except Exception as e:
                st.error(f"⚠️ GPT failed: {e}")

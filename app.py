import streamlit as st
from core.resume_parser import parse_resume
from core.matching_engine import compare_keywords
from core.openrouter_engine import generate_resume_summary
from core.docx_exporter import generate_docx

# ---------- UI Setup ----------
st.set_page_config(page_title="AI Resume Tailor", layout="centered")
st.title("📄 AI Resume Tailor")
st.caption("Tailor your resume to any job description using AI.")

# ---------- Upload Inputs ----------
resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
job_description = st.text_area("Paste the job description here")


# ---------- UI Keyword Bubble Style ----------
def display_keywords(title, keywords, color):
    st.markdown(f"### {title}")
    if not keywords:
        st.success("✨ You're good! Nothing missing.")
    else:
        keyword_line = ", ".join(sorted(keywords))
        st.markdown(f"""
        <div style='
            background-color: {color};
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: bold;'>
            {keyword_line}
        </div>
        """, unsafe_allow_html=True)


# ---------- Main Resume Processing ----------
if st.button("✨ Tailor My Resume"):
    if not resume_file:
        st.warning("Please upload your resume first.")
    elif not job_description.strip():
        st.warning("Please paste the job description.")
    else:
        resume_text = parse_resume(resume_file)
        matched, missing = compare_keywords(resume_text, job_description)

        st.success("✅ Resume parsed and compared!")

        display_keywords("✅ Matched Keywords", matched, "#2ECC71")
        display_keywords("❌ Missing Important Keywords", missing, "#E74C3C")

        # ----------- GPT Summary + Skills -----------
        with st.spinner("🤖 Generating AI-tailored summary and skills..."):
            try:
                response = generate_resume_summary(resume_text, job_description)

                if "### Skills Section:" in response:
                    summary, skills_raw = response.split("### Skills Section:")
                else:
                    summary = response
                    skills_raw = ""

                skills = [line.strip("- ").strip() for line in skills_raw.strip().split("\n") if line.strip()]

                st.markdown("### 🧠 Tailored Summary")
                st.info(summary)

                st.markdown("### 💼 Suggested Skills Section")
                if skills:
                    st.success(", ".join(skills))
                else:
                    st.info("No skills generated.")

                # ----------- Text Download -----------
                report = "AI Resume Tailor Report\n\n"
                report += "✅ Matched Keywords:\n" + (", ".join(sorted(matched)) if matched else "None")
                report += "\n\n❌ Missing Important Keywords:\n" + (", ".join(sorted(missing)) if missing else "None")
                report += "\n\n🧠 Summary:\n" + summary
                report += "\n\n💼 Skills:\n" + (", ".join(skills) if skills else "None")

                st.download_button(
                    label="⬇️ Download Report (.txt)",
                    data=report,
                    file_name="resume_tailor_report.txt",
                    mime="text/plain"
                )

                # ----------- DOCX Download -----------
                docx_file = generate_docx(summary, skills, matched, missing)
                st.download_button(
                    label="⬇️ Download Full Resume Report (.docx)",
                    data=docx_file,
                    file_name="resume_tailor_report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            except Exception as e:
                st.error(f"⚠️ GPT failed: {e}")

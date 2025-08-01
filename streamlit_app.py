import streamlit as st
import re
from backend.job_loader import load_jobs_from_csv
from backend.praser import extract_resumes
from backend.embedder import match_resumes_to_job

st.title("GenAI Resume Screener")

def extract_name(text):
    # Look for patterns like Name: Mark Griffin or name=Mark Griffin (case-insensitive)
    match = re.search(r'name\s*[:=]\s*([A-Za-z .\-]+)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: first short line
    lines = text.split('\n')
    for line in lines:
        if line.strip() and len(line.strip().split()) <= 5:
            return line.strip()
    return "Unknown"

def extract_contact(text):
    # Extract email and phone number using regex
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', text)
    email_str = email.group(0) if email else "Not found"
    phone_str = phone.group(0) if phone else "Not found"
    return f"Email: {email_str}, Phone: {phone_str}"

# Upload job description CSV
job_csv = st.file_uploader("Upload Job Description CSV", type=["csv"])
resume_folder = st.text_input("Path to Resume Folder", value=r"Resource/CVs1")

if job_csv and resume_folder:
    jobs = load_jobs_from_csv(job_csv)
    resume_texts = extract_resumes(resume_folder)
    resumes = [{"filename": fn, "text": txt} for fn, txt in resume_texts.items()]

    job_title = st.selectbox("Select Job Title", list(jobs.keys()))
    if st.button("Match Resumes"):
        with st.spinner("🔎 Matching in progress..."):
            job_desc = jobs[job_title]
            matches = match_resumes_to_job(job_desc, resumes)
        st.success("✅ Matching complete!")
        st.subheader("Top Matching Resumes")
        for resume, score in matches[:5]:
            name = extract_name(resume["text"])
            contact = extract_contact(resume["text"])
            st.write(f"**File:** {resume['filename']}  \n**Name:** {name}  \n**Contact:** {contact}  \n**Score:** {score.item():.4f}")
            with st.expander("Show Resume Text"):
                st.write(resume["text"][:1000])  # Show first 1000 chars

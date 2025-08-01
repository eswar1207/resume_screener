import os
from backend.job_loader import load_jobs_from_csv
from backend.praser import extract_resumes
from backend.embedder import match_resumes_to_job

def main():
    # Load job descriptions
    job_csv = r"C:\Users\siva\projects\genai_resume_screener\Resource\job_description.csv"
    jobs = load_jobs_from_csv(job_csv)

    # Extract resumes
    resume_folder = r"C:\Users\siva\projects\genai_resume_screener\Resource\CVs1"
    resume_texts = extract_resumes(resume_folder)
    resumes = [{"filename": fn, "text": txt} for fn, txt in resume_texts.items()]

    # For each job, match resumes
    for job_title, job_desc in jobs.items():
        print(f"\n=== Matching resumes for job: {job_title} ===")
        matches = match_resumes_to_job(job_desc, resumes)
        for resume, score in matches[:5]:  # Show top 5 matches
            print(f"Resume: {resume['filename']} | Score: {score.item():.4f}")

if __name__ == "__main__":
    main()
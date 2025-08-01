import pandas as pd

def load_jobs_from_csv(csv_path):
    df = pd.read_csv(csv_path, encoding='cp1252')
    
    # Drop any unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    jobs = {}
    for _, row in df.iterrows():
        if pd.notna(row['Job Title']) and pd.notna(row['Job Description']):
            title = row['Job Title']
            desc = row['Job Description']
            jobs[title] = desc
    return jobs


if __name__ == "__main__":
    jobs = load_jobs_from_csv(r"C:\Users\siva\projects\genai_resume_screener\Resource\job_description.csv")    
    for title, description in jobs.items():
        print(title)
        print(description[:])  # Preview first 200 characters
        print("-" * 50)  # Separator line
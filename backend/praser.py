import os
import fitz

def extract_text_from_pdf(pdf_path):
    text=""
    doc=fitz.open(pdf_path)
    for page in doc:
        text+=page.get_text()
    return text

def extract_resumes(resume_folder):
    resume_data={}
    for file in os.listdir(resume_folder):
        if file.endswith(".pdf"):
            path=os.path.join(resume_folder,file)
            text=extract_text_from_pdf(path)
            resume_data[file]=text
    return resume_data

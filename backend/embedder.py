# matcher.py
from sentence_transformers import SentenceTransformer, util

# Use a stronger model for semantic matching
model = SentenceTransformer('BAAI/bge-base-en-v1.5')  # Correct HuggingFace model name

def get_embeddings(texts):
    # Normalize embeddings for better cosine similarity
    return model.encode(texts, convert_to_tensor=True, normalize_embeddings=True)

def match_resumes_to_job(job_desc, resumes):
    job_embedding = get_embeddings([job_desc])[0]
    resume_texts = [res["text"] for res in resumes]
    resume_embeddings = get_embeddings(resume_texts)
    
    scores = util.cos_sim(job_embedding, resume_embeddings)[0]
    matched = sorted(zip(resumes, scores), key=lambda x: x[1], reverse=True)
    return matched

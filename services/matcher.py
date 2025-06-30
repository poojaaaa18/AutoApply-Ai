import spacy
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import faiss

# Load spaCy and model once
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
stop_words = nlp.Defaults.stop_words
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

def clean_text(text):
    text = re.sub(r'\n\s*\n|\n||LINK', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and not token.is_punct]
    return ' '.join(tokens)

def extract_sections(text):
    sections = {}
    current_section = None
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.isupper():
            current_section = line
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
    
    weights = {'SKILLS': 0.5, 'PROJECTS': 0.3, 'EXPERIENCE': 0.2}
    weighted_text = []
    for section, weight in weights.items():
        if section in sections:
            section_text = ' '.join(sections[section])
            weighted_text.extend([section_text] * int(weight * 10))
    combined_text = ' '.join(weighted_text)
    return combined_text if combined_text else text

def keyword_match(resume_text, job_text):
    resume_keywords = set(clean_text(resume_text).split())
    job_keywords = set(clean_text(job_text).split())
    if not job_keywords:
        return 0.0
    return len(resume_keywords.intersection(job_keywords)) / len(job_keywords)

def matcher(resume_data, job_descriptions, top_k=5):
    resume_text = resume_data['parsed_resume']
    relevant_resume_text = extract_sections(resume_text)
    cleaned_resume = clean_text(relevant_resume_text)

    cleaned_jobs = [clean_text(jd) for jd in job_descriptions]
    resume_embedding = model.encode([cleaned_resume], show_progress_bar=False)[0]
    job_embeddings = model.encode(cleaned_jobs, show_progress_bar=False)

    dimension = job_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(job_embeddings)

    k = min(top_k, len(job_descriptions))
    distances, indices = index.search(np.array([resume_embedding]), k)

    job_embeddings_np = np.array(job_embeddings)
    resume_embedding_np = np.array([resume_embedding])
    cosine_similarities = cosine_similarity(resume_embedding_np, job_embeddings_np)[0]

    results = []
    for idx in indices[0]:
        semantic_score = cosine_similarities[idx]
        keyword_score = keyword_match(relevant_resume_text, job_descriptions[idx])
        final_score = 0.7 * semantic_score + 0.3 * keyword_score
        resume_keywords = set(clean_text(relevant_resume_text).split())
        job_keywords = set(clean_text(job_descriptions[idx]).split())
        matched_keywords = resume_keywords.intersection(job_keywords)

        results.append({
            'job': job_descriptions[idx],
            'semantic_score': semantic_score,
            'keyword_score': keyword_score,
            'final_score': final_score,
            'matched_keywords': matched_keywords
        })

    return sorted(results, key=lambda x: x['final_score'], reverse=True)


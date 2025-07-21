import nltk
from nltk.corpus import stopwords

# Download stopwords only if not present
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Lowercase and remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text

def extract_keywords(text):
    # Remove stopwords and split
    text = clean_text(text)
    words = [word for word in text.split() if word not in stop_words and len(word) > 2]
    return set(words)

def compare_keywords(resume_text, job_desc_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_desc_text)

    matched = resume_keywords.intersection(jd_keywords)
    missing = jd_keywords - resume_keywords

    return list(matched), list(missing)

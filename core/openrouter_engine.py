import os
import requests
from dotenv import load_dotenv

def generate_resume_summary(resume_text, job_description):
    load_dotenv()

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mixtral-8x7b-instruct")

    if not OPENROUTER_API_KEY:
        raise ValueError("🚨 OPENROUTER_API_KEY not found in .env file")

    prompt = f"""
You are a professional resume consultant.

Given the resume and job description below, generate the following two sections clearly and exactly in this format:

### Professional Summary:
<3–5 lines summarizing the candidate tailored to the job>

### Skills Section:
- skill 1
- skill 2
- skill 3
(Include any relevant or missing skills from the job description)

Resume:
{resume_text}

Job Description:
{job_description}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"OpenRouter API Error: {response.status_code} - {response.text}")

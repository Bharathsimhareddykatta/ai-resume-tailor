import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mixtral-8x7b-instruct")
TIMEOUT = 45  # seconds

if not OPENROUTER_API_KEY:
    raise ValueError("🚨 OPENROUTER_API_KEY not found in .env file")


def generate_resume_summary(resume_text, job_description):
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

    # Retry logic
    for attempt in range(3):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body,
                timeout=TIMEOUT
            )

            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
            else:
                raise Exception(f"OpenRouter API Error: {response.status_code} - {response.text}")

        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout on attempt {attempt + 1}. Retrying...")
            time.sleep(2)

    raise Exception("❌ OpenRouter API failed after 3 retries due to timeout.")

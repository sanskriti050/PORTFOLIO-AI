import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================================
# COMMON GROQ FUNCTION
# ==========================================================

def ask_ai(prompt, temperature=0.2):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=temperature
    )

    return response.choices[0].message.content.strip()
# ==========================================================
# PORTFOLIO JSON GENERATOR
# ==========================================================

def generate_portfolio_json(resume_text):

    prompt = f"""
You are an expert resume parser.

Convert the following resume into ONLY valid JSON.

Rules:

- Return ONLY JSON.
- No markdown.
- No explanation.
- No extra text.

Structure:

{{
    "name":"",
    "headline":"",
    "about":"",
    "skills":[],
    "projects":[],
    "education":[],
    "experience":[],
    "certifications":[],
    "github":"",
    "linkedin":"",
    "email":"",
    "phone":""
}}

Resume:

{resume_text}
"""

    text = ask_ai(prompt)

    # ==========================================
    # Remove Markdown
    # ==========================================

    text = text.strip()

    if text.startswith("```json"):

        text = text.replace("```json", "")

    if text.startswith("```"):

        text = text.replace("```", "")

    if text.endswith("```"):

        text = text.replace("```", "")

    text = text.strip()

    # ==========================================
    # Parse JSON
    # ==========================================

    try:

        data = json.loads(text)

    except Exception:

        start = text.find("{")

        end = text.rfind("}") + 1

        if start != -1 and end != -1:

            data = json.loads(text[start:end])

        else:

            raise Exception(
                "AI returned invalid JSON."
            )

    # ==========================================
    # Ensure All Keys Exist
    # ==========================================

    defaults = {

        "name": "",

        "headline": "",

        "about": "",

        "skills": [],

        "projects": [],

        "education": [],

        "experience": [],

        "certifications": [],

        "github": "",

        "linkedin": "",

        "email": "",

        "phone": ""

    }

    for key, value in defaults.items():

        if key not in data:

            data[key] = value

    return data

# ==========================================================
# AI RESUME REVIEW
# ==========================================================

def review_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer.

Review the following resume professionally.

Return the response in Markdown.

Use the following structure:

# Resume Score (out of 100)

# Strengths

- Point 1
- Point 2
- Point 3

# Weaknesses

- Point 1
- Point 2
- Point 3

# ATS Improvements

- Point 1
- Point 2
- Point 3

# Technical Suggestions

- Point 1
- Point 2

# HR Suggestions

- Point 1
- Point 2

Resume:

{resume_text}
"""

    return ask_ai(
        prompt,
        temperature=0.3
    )

# ==========================================================
# AI RESUME IMPROVER
# ==========================================================

def improve_resume(resume_text):

    prompt = f"""
You are a Senior Resume Writer and ATS Expert.

Rewrite the following resume professionally.

Requirements:

- Keep all original information.
- Improve grammar and wording.
- Make it ATS-friendly.
- Use strong action verbs.
- Improve project descriptions.
- Improve summary.
- Improve skills section.
- Improve formatting.
- Do NOT invent fake experience or projects.
- Return the response in Markdown format.

Structure:

# Professional Summary

# Technical Skills

# Projects

# Experience

# Education

# Certifications

Resume:

{resume_text}
"""

    return ask_ai(
        prompt,
        temperature=0.4
    )

# ==========================================================
# AI COVER LETTER GENERATOR
# ==========================================================

def generate_cover_letter(resume_text, company_name="Your Company"):

    prompt = f"""
You are an expert HR Recruiter and Professional Resume Writer.

Using the resume below, write a professional cover letter.

Requirements:

- Address the company as "{company_name}".
- Keep it within 300-400 words.
- Use a professional tone.
- Highlight the candidate's technical skills.
- Mention projects naturally.
- Mention enthusiasm for the role.
- End with a professional closing.
- Do NOT invent fake experience.
- Return ONLY the cover letter in Markdown.

Resume:

{resume_text}
"""

    return ask_ai(
        prompt,
        temperature=0.5
    )

# ==========================================================
# AI INTERVIEW QUESTION GENERATOR
# ==========================================================

def generate_interview_questions(resume_text):

    prompt = f"""
You are an experienced Technical Interviewer.

Based on the candidate's resume, generate interview questions.

Return the response in Markdown.

Use this structure:

# Technical Questions

1.
2.
3.
4.
5.

# Project Based Questions

1.
2.
3.
4.
5.

# HR Questions

1.
2.
3.
4.
5.

# Coding Questions

1.
2.
3.
4.
5.

# Preparation Tips

- Tip 1
- Tip 2
- Tip 3
- Tip 4
- Tip 5

Resume:

{resume_text}
"""

    return ask_ai(
        prompt,
        temperature=0.4
    )
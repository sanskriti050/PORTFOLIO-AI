import os
import json
import requests

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# GROQ CLIENT
# ==========================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.3-70b-versatile"

# ==========================================================
# COMMON AI FUNCTION
# ==========================================================

def ask_ai(prompt, temperature=0.2):

    response = client.chat.completions.create(

        model=MODEL,

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
# CLEAN JSON
# ==========================================================

def clean_json(text):

    text = text.strip()

    if text.startswith("```json"):

        text = text.replace("```json", "")

    if text.startswith("```"):

        text = text.replace("```", "")

    if text.endswith("```"):

        text = text[:-3]

    return text.strip()


# ==========================================================
# PORTFOLIO JSON
# ==========================================================

def generate_portfolio_json(resume_text):

    prompt = f"""
You are an expert Resume Parser.

Convert the resume into ONLY valid JSON.

Return ONLY JSON.

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

    response = ask_ai(prompt)

    response = clean_json(response)

    return json.loads(response)


# ==========================================================
# RESUME REVIEW
# ==========================================================

def review_resume(resume_text):

    prompt = f"""
You are a Senior Technical Recruiter.

Review the following resume.

Give:

1. Overall Score /100

2. ATS Score

3. Strong Points

4. Weak Points

5. Missing Skills

6. Grammar Suggestions

7. Formatting Suggestions

8. Final Verdict

Resume:

{resume_text}
"""

    return ask_ai(
        prompt,
        temperature=0.4
    )
# ==========================================================
# IMPROVE RESUME
# ==========================================================

def improve_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Writer.

Rewrite the following resume professionally.

Rules:

- ATS Friendly
- Better Bullet Points
- Strong Action Verbs
- Professional Formatting
- Do not invent fake experience.
- Return only the improved resume.

Resume:

{resume_text}
"""

    return ask_ai(
        prompt,
        temperature=0.4
    )


# ==========================================================
# COVER LETTER
# ==========================================================

def generate_cover_letter(resume_text):

    prompt = f"""
Generate a professional cover letter based on this resume.

Keep it:

- Professional
- One Page
- Suitable for Software Engineer / AI / ML roles

Resume:

{resume_text}
"""

    return ask_ai(
        prompt,
        temperature=0.5
    )


# ==========================================================
# INTERVIEW QUESTIONS
# ==========================================================

def generate_interview_questions(resume_text):

    prompt = f"""
Based on this resume generate interview questions.

Include:

Technical Questions

Project Questions

HR Questions

Behavioral Questions

Coding Questions

Resume:

{resume_text}
"""

    return ask_ai(
        prompt,
        temperature=0.5
    )


# ==========================================================
# GITHUB PROFILE
# ==========================================================

def get_github_profile(username):

    if not username:

        return None

    try:

        url = f"https://api.github.com/users/{username}"

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:

            return None

        data = response.json()

        return {

            "name": data.get("name"),

            "login": data.get("login"),

            "bio": data.get("bio"),

            "followers": data.get("followers"),

            "following": data.get("following"),

            "public_repos": data.get("public_repos"),

            "avatar_url": data.get("avatar_url"),

            "html_url": data.get("html_url")

        }

    except Exception:

        return None


# ==========================================================
# LEETCODE PROFILE
# ==========================================================

def get_leetcode_profile(username):

    if not username:

        return None

    try:

        return {

            "username": username,

            "profile": f"https://leetcode.com/{username}/",

            "solved": "N/A",

            "ranking": "N/A"

        }

    except Exception:

        return None


# ==========================================================
# HEALTH CHECK
# ==========================================================

def check_api():

    try:

        ask_ai("Reply with only OK.")

        return True

    except Exception:

        return False
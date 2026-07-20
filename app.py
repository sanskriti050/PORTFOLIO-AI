import json
import os
import webbrowser

import streamlit as st
import streamlit.components.v1 as components

from parser import extract_text
from ai import (
    generate_portfolio_json,
    review_resume,
    improve_resume,
    generate_cover_letter,
    generate_interview_questions
)

from generator import generate_portfolio

from styles import load_css

from components import (
    hero,
    stats,
    feature_cards,
    footer,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="PortfolioAI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# LOAD CUSTOM CSS
# ==========================================================

st.markdown(
    load_css(),
    unsafe_allow_html=True,
)

# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULT_SESSION = {

    "resume_text": "",

    "portfolio_data": None,

    "portfolio_file": None,

    "resume_review": "",

    "improved_resume": "",

    "cover_letter": "",

    "theme": "Modern",

    "generated": False,

    "error": None,

}

for key, value in DEFAULT_SESSION.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================================
# PAGE HEADER
# ==========================================================

hero()

stats()

st.markdown("<br>", unsafe_allow_html=True)

feature_cards()

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# PAGE TITLE
# ==========================================================

st.markdown(
    """
    <h2 style='text-align:center;'>
        🚀 AI Powered Portfolio Generator
    </h2>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Upload your resume and let AI build a professional portfolio website, review your resume, improve content and generate a cover letter."
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# MAIN DASHBOARD
# ==========================================================

left, right = st.columns([1, 1.25], gap="large")

# ==========================================================
# LEFT PANEL
# ==========================================================

with left:

    st.markdown("## 📄 Upload Resume")

    st.caption(
        "Upload your PDF or DOCX resume and let AI generate a complete developer portfolio."
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # THEME
    # ======================================================

    st.markdown("### 🎨 Portfolio Theme")

    theme = st.selectbox(
        "Theme",
        [
            "Modern",
            "Glass",
            "Dark",
            "Minimal",
            "Cyberpunk",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.session_state.theme = theme

    theme_info = {

        "Modern":
        "✨ Clean and professional recruiter-friendly portfolio.",

        "Glass":
        "💎 Premium glassmorphism UI with elegant cards.",

        "Dark":
        "🌙 Dark developer portfolio inspired by modern SaaS websites.",

        "Minimal":
        "📄 Simple, elegant and distraction-free layout.",

        "Cyberpunk":
        "🚀 Neon futuristic developer portfolio.",
    }

    st.info(theme_info[theme])

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # AI STATUS
    # ======================================================

    st.markdown("### 🤖 AI Status")

    if st.session_state.generated:

        st.success("✅ Portfolio Generated Successfully")

    else:

        st.warning("Waiting for Resume Upload")

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # GENERATE BUTTON
    # ======================================================

    generate = st.button(
        "🚀 Generate Portfolio",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # QUICK INFO
    # ======================================================

    st.markdown("### 📌 What AI Generates")

    st.success("""
✅ Portfolio Website

✅ Resume Review

✅ Resume Improvement

✅ Cover Letter

✅ Portfolio JSON

✅ Live Preview
""")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### ⚡ AI Pipeline")

    st.write("1️⃣ Read Resume")

    st.write("2️⃣ Extract Information")

    st.write("3️⃣ Generate Portfolio")

    st.write("4️⃣ Review Resume")

    st.write("5️⃣ Improve Resume")

    st.write("6️⃣ Generate Cover Letter")

# ==========================================================
# RIGHT PANEL
# ==========================================================

with right:

    st.markdown("## 👀 Live Portfolio Preview")

    st.caption(
        "Your AI-generated portfolio will appear here instantly after generation."
    )

    # ======================================================
    # IF PORTFOLIO EXISTS
    # ======================================================

    if (
        st.session_state.generated
        and st.session_state.portfolio_file
        and os.path.exists(st.session_state.portfolio_file)
    ):

        try:

            with open(
                st.session_state.portfolio_file,
                "r",
                encoding="utf-8",
            ) as f:

                html = f.read()

            components.html(
                html,
                height=750,
                scrolling=True,
            )

            st.success("✅ Live Portfolio Preview Ready")

        except Exception as e:

            st.error(f"Unable to load preview.\n\n{e}")

    # ======================================================
    # PLACEHOLDER
    # ======================================================

    else:

        st.info(
            "Generate your portfolio to see the live preview."
        )

        st.image(
            "https://placehold.co/900x550/111827/FFFFFF?text=AI+Portfolio+Preview",
            use_container_width=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### 🚀 Preview Includes")

        col1, col2 = st.columns(2)

        with col1:

            st.success("""
👤 Hero Section

📖 About

🛠 Skills

💼 Projects
""")

        with col2:

            st.success("""
🎓 Education

📜 Certifications

📞 Contact

🌐 Responsive Design
""")

        st.markdown("<br>", unsafe_allow_html=True)

        st.warning(
            "Preview will automatically update after AI generates your portfolio."
        )
# ==========================================================
# GENERATE PORTFOLIO
# ==========================================================

if generate:

    # Reset old values

    st.session_state.generated = False
    st.session_state.error = None
    st.session_state.portfolio_file = None
    st.session_state.portfolio_data = None
    st.session_state.resume_review = ""
    st.session_state.improved_resume = ""
    st.session_state.cover_letter = ""

    if uploaded_file is None:

        st.warning("⚠ Please upload your resume first.")

    else:

        try:

            progress = st.progress(0)

            status = st.empty()

            # =====================================
            # STEP 1
            # =====================================

            status.info("📄 Reading Resume...")

            resume_text = extract_text(uploaded_file)

            st.session_state.resume_text = resume_text

            progress.progress(15)

            # =====================================
            # STEP 2
            # =====================================

            status.info("🤖 Extracting Resume Information...")

            portfolio_data = generate_portfolio_json(
                resume_text
            )

            st.session_state.portfolio_data = portfolio_data

            progress.progress(35)

            # =====================================
            # STEP 3
            # =====================================

            status.info("🎨 Building Portfolio Website...")

            portfolio_file = generate_portfolio(
                portfolio_data,
                st.session_state.theme
            )

            st.session_state.portfolio_file = portfolio_file

            progress.progress(55)

            # =====================================
            # STEP 4
            # =====================================

            status.info("📝 Reviewing Resume...")

            review = review_resume(
                resume_text
            )

            st.session_state.resume_review = review

            progress.progress(70)

            # =====================================
            # STEP 5
            # =====================================

            status.info("✨ Improving Resume...")

            improved = improve_resume(
                resume_text
            )

            st.session_state.improved_resume = improved

            progress.progress(85)

            # =====================================
            # STEP 6
            # =====================================

            status.info("💌 Generating Cover Letter...")

            cover = generate_cover_letter(
                resume_text
            )

            st.session_state.cover_letter = cover

            progress.progress(100)

            # =====================================
            # COMPLETE
            # =====================================

            st.session_state.generated = True

            status.success(
                "🎉 Portfolio Generated Successfully!"
            )

            st.balloons()

            st.rerun()

        except Exception as e:

            st.session_state.generated = False

            st.session_state.error = str(e)

            st.error(f"❌ {e}")
    # ==========================================================
# AI RESULTS DASHBOARD
# ==========================================================

if st.session_state.generated:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    st.header("🤖 AI Results Dashboard")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📄 Resume",
            "🌐 Portfolio Data",
            "📝 Resume Review",
            "✨ Improved Resume",
            "💌 Cover Letter",
        ]
    )

    # ======================================================
    # TAB 1
    # ======================================================

    with tab1:

        st.subheader("📄 Extracted Resume")

        st.text_area(
            "",
            st.session_state.resume_text,
            height=450,
        )

    # ======================================================
    # TAB 2
    # ======================================================

    with tab2:

        st.subheader("🌐 Portfolio JSON")

        st.json(
            st.session_state.portfolio_data
        )

    # ======================================================
    # TAB 3
    # ======================================================

    with tab3:

        st.subheader("📝 AI Resume Review")

        st.markdown(
            st.session_state.resume_review
        )

    # ======================================================
    # TAB 4
    # ======================================================

    with tab4:

        st.subheader("✨ Improved Resume")

        st.text_area(
            "",
            st.session_state.improved_resume,
            height=500,
        )

    # ======================================================
    # TAB 5
    # ======================================================

    with tab5:

        st.subheader("💌 AI Generated Cover Letter")

        st.text_area(
            "",
            st.session_state.cover_letter,
            height=500,
        )
    # ==========================================================
# PORTFOLIO ANALYTICS
# ==========================================================

if st.session_state.generated:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    st.header("📊 Portfolio Analytics")

    data = st.session_state.portfolio_data

    # --------------------------------------------
    # SAFE COUNTS
    # --------------------------------------------

    skills = data.get("skills", [])
    projects = data.get("projects", [])
    education = data.get("education", [])
    experience = data.get("experience", [])
    certifications = data.get("certifications", [])

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "💻 Skills",
            len(skills)
        )

    with c2:
        st.metric(
            "📂 Projects",
            len(projects)
        )

    with c3:
        st.metric(
            "🏢 Experience",
            len(experience)
        )

    with c4:
        st.metric(
            "🎓 Education",
            len(education)
        )

    with c5:
        st.metric(
            "📜 Certificates",
            len(certifications)
        )

    st.markdown("---")

    # --------------------------------------------
    # BASIC INFO
    # --------------------------------------------

    st.subheader("👤 Candidate Information")

    info1, info2 = st.columns(2)

    with info1:

        st.success(f"**Name:** {data.get('name','-')}")

        st.info(f"**Headline:** {data.get('headline','-')}")

        st.write(f"📧 {data.get('email','-')}")

        st.write(f"📱 {data.get('phone','-')}")

    with info2:

        st.write("### 🔗 Social Links")

        github = data.get("github", "")
        linkedin = data.get("linkedin", "")

        if github:
            st.markdown(f"**GitHub:** {github}")

        if linkedin:
            st.markdown(f"**LinkedIn:** {linkedin}")

    st.markdown("---")

    # --------------------------------------------
    # SKILLS
    # --------------------------------------------

    st.subheader("💻 Detected Skills")

    if skills:

        cols = st.columns(4)

        for i, skill in enumerate(skills):

            cols[i % 4].success(skill)

    else:

        st.info("No skills detected.")

    st.markdown("---")

    # --------------------------------------------
    # PROJECTS
    # --------------------------------------------

    st.subheader("📂 Projects")

    if projects:

        for project in projects:

            if isinstance(project, dict):

                title = project.get(
                    "title",
                    project.get("name", "Project")
                )

                desc = project.get(
                    "description",
                    "No description available."
                )

                with st.expander(title):

                    st.write(desc)

                    tech = project.get(
                        "tech_stack",
                        []
                    )

                    if tech:

                        st.write("**Tech Stack**")

                        st.write(", ".join(tech))

            else:

                st.write(project)

    else:

        st.info("No projects found.")

    st.markdown("---")

    # --------------------------------------------
    # EDUCATION
    # --------------------------------------------

    st.subheader("🎓 Education")

    if education:

        for edu in education:

            if isinstance(edu, dict):

                st.success(
                    f"{edu.get('degree','')} | {edu.get('institute','')} | {edu.get('year','')}"
                )

            else:

                st.success(edu)

    else:

        st.info("No education found.")

    st.markdown("---")

    # --------------------------------------------
    # EXPERIENCE
    # --------------------------------------------

    st.subheader("🏢 Experience")

    if experience:

        for exp in experience:

            if isinstance(exp, dict):

                with st.expander(
                    exp.get("role", "Experience")
                ):

                    st.write(
                        f"**Company:** {exp.get('company','-')}"
                    )

                    st.write(
                        f"**Duration:** {exp.get('duration','-')}"
                    )

            else:

                st.write(exp)

    else:

        st.info("No experience detected.")

    st.markdown("---")

    # --------------------------------------------
    # CERTIFICATIONS
    # --------------------------------------------

    st.subheader("📜 Certifications")

    if certifications:

        for cert in certifications:

            if isinstance(cert, dict):

                st.success(
                    cert.get("title", "-")
                )

            else:

                st.success(cert)

    else:

        st.info("No certifications found.")
    # ==========================================================
# EXPORT CENTER
# ==========================================================

if st.session_state.generated:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    st.header("📥 Export Portfolio")

    col1, col2, col3, col4 = st.columns(4)

    # ==========================================
    # DOWNLOAD HTML
    # ==========================================

    with col1:

        with open(
            st.session_state.portfolio_file,
            "r",
            encoding="utf-8"
        ) as f:

            html = f.read()

        st.download_button(
            label="📄 Download HTML",
            data=html,
            file_name="index.html",
            mime="text/html",
            use_container_width=True
        )

    # ==========================================
    # DOWNLOAD JSON
    # ==========================================

    with col2:

        st.download_button(

            label="🤖 Download JSON",

            data=json.dumps(
                st.session_state.portfolio_data,
                indent=4
            ),

            file_name="portfolio.json",

            mime="application/json",

            use_container_width=True
        )

    # ==========================================
    # OPEN PORTFOLIO
    # ==========================================

    with col3:

        if st.button(
            "🌐 Open Portfolio",
            use_container_width=True
        ):

            webbrowser.open(
                "file://" + os.path.abspath(
                    st.session_state.portfolio_file
                )
            )

            st.success("Portfolio opened successfully.")

    # ==========================================
    # DOWNLOAD RESUME
    # ==========================================

    with col4:

        st.download_button(

            label="📄 Resume.txt",

            data=st.session_state.resume_text,

            file_name="resume.txt",

            mime="text/plain",

            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # QUICK EXPORT INFO
    # ==========================================================

    st.success("""
### ✅ Generated Files

📄 index.html

🤖 portfolio.json

📄 resume.txt

🌐 Live Portfolio Preview
""")

    # ==========================================================
    # EXPORT SUMMARY
    # ==========================================================

    with st.expander("📦 Export Summary", expanded=False):

        st.write("Your generated portfolio package contains:")

        st.markdown("""
- ✅ Responsive HTML Portfolio
- ✅ AI Extracted Portfolio JSON
- ✅ Resume Text
- ✅ Live Preview
- ✅ Ready for GitHub Pages
- ✅ Ready for Netlify
- ✅ Ready for Vercel
""")

        st.info(
            "Upcoming Update: ZIP Download, One-click GitHub Deployment and Netlify Export."
        )
    # ==========================================================
# AI ANALYTICS DASHBOARD
# ==========================================================

if st.session_state.generated:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    st.header("📈 AI Analytics Dashboard")

    data = st.session_state.portfolio_data

    skills = data.get("skills", [])
    projects = data.get("projects", [])
    experience = data.get("experience", [])
    education = data.get("education", [])
    certifications = data.get("certifications", [])

    # =====================================================
    # SCORE CARDS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "💻 Skills",
            len(skills)
        )

    with c2:
        st.metric(
            "📂 Projects",
            len(projects)
        )

    with c3:
        st.metric(
            "🏢 Experience",
            len(experience)
        )

    with c4:
        st.metric(
            "📜 Certificates",
            len(certifications)
        )

    st.markdown("---")

    # =====================================================
    # PROFILE COMPLETENESS
    # =====================================================

    st.subheader("✅ Profile Completeness")

    score = 0

    if data.get("name"):
        score += 10

    if data.get("headline"):
        score += 10

    if skills:
        score += 20

    if projects:
        score += 20

    if experience:
        score += 15

    if education:
        score += 15

    if certifications:
        score += 5

    if data.get("github"):
        score += 3

    if data.get("linkedin"):
        score += 2

    st.progress(score / 100)

    st.success(f"Portfolio Completeness : {score}%")

    st.markdown("---")

    # =====================================================
    # AI RECOMMENDATIONS
    # =====================================================

    st.subheader("🤖 AI Suggestions")

    suggestions = []

    if len(skills) < 5:
        suggestions.append(
            "➕ Add more technical skills."
        )

    if len(projects) < 3:
        suggestions.append(
            "📂 Add more projects."
        )

    if len(experience) == 0:
        suggestions.append(
            "💼 Add internship or experience."
        )

    if len(certifications) == 0:
        suggestions.append(
            "📜 Add certifications."
        )

    if not data.get("github"):
        suggestions.append(
            "🔗 Add GitHub profile."
        )

    if not data.get("linkedin"):
        suggestions.append(
            "💼 Add LinkedIn profile."
        )

    if suggestions:

        for item in suggestions:

            st.warning(item)

    else:

        st.success(
            "Excellent! Your portfolio looks strong."
        )

    st.markdown("---")

    # =====================================================
    # RESUME STRENGTH
    # =====================================================

    st.subheader("🚀 Resume Strength")

    strengths = [
        ("Skills", len(skills), 10),
        ("Projects", len(projects), 6),
        ("Experience", len(experience), 3),
        ("Education", len(education), 2),
        ("Certifications", len(certifications), 5),
    ]

    for title, value, target in strengths:

        percentage = min(value / target, 1.0)

        st.write(title)

        st.progress(percentage)

        st.caption(f"{value} / {target}")

    st.markdown("---")

    # =====================================================
    # PROFILE SUMMARY
    # =====================================================

    st.subheader("👤 Candidate Summary")

    st.info(f"""
### {data.get("name","Unknown")}

**Headline**

{data.get("headline","Not Available")}

**Email**

{data.get("email","-")}

**Phone**

{data.get("phone","-")}
""")

    st.markdown("---")

    # =====================================================
    # AI BADGES
    # =====================================================

    st.subheader("🏅 AI Portfolio Badges")

    b1, b2, b3 = st.columns(3)

    with b1:

        if len(projects) >= 3:

            st.success("🚀 Project Ready")

        else:

            st.warning("Need More Projects")

    with b2:

        if len(skills) >= 8:

            st.success("💻 Skill Expert")

        else:

            st.warning("Need More Skills")

    with b3:

        if data.get("github"):

            st.success("🌐 GitHub Ready")

        else:

            st.warning("GitHub Missing")
    # ==========================================================
# ERROR PANEL
# ==========================================================

if st.session_state.error:

    st.markdown("<br>", unsafe_allow_html=True)

    st.error("❌ Something went wrong while generating the portfolio.")

    with st.expander("🐞 Show Error Details"):

        st.code(
            st.session_state.error,
            language="text"
        )

# ==========================================================
# QUICK TIPS
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

st.header("💡 Tips for Better Portfolio")

tip1, tip2 = st.columns(2)

with tip1:

    st.success("""
### ✅ Resume Tips

- Use ATS Friendly Resume

- Add 3-5 Projects

- Mention Technical Skills

- Keep GitHub Updated

- Add LinkedIn Profile

- Mention Certifications

- Add Internship Experience
""")

with tip2:

    st.info("""
### 🚀 Portfolio Tips

- Upload latest resume

- Keep project descriptions clear

- Mention tech stack

- Add achievements

- Include GitHub links

- Use professional headline

- Add contact information
""")

# ==========================================================
# FEATURE ROADMAP
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

st.header("🛣 Roadmap")

road1, road2 = st.columns(2)

with road1:

    st.success("""
### ✅ Current Features

✔ Resume Parsing

✔ AI Portfolio Generation

✔ Live Preview

✔ Resume Review

✔ Resume Improvement

✔ Cover Letter

✔ HTML Download

✔ JSON Export

✔ Portfolio Analytics
""")

with road2:

    st.warning("""
### 🚀 Upcoming Features

⬜ ZIP Download

⬜ GitHub Deployment

⬜ Netlify Deployment

⬜ Portfolio Themes

⬜ Dark / Light Mode

⬜ AI Chat Assistant

⬜ Portfolio Hosting

⬜ Resume ATS Score

⬜ AI Interview Questions
""")

# ==========================================================
# FAQ
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

st.header("❓ Frequently Asked Questions")

with st.expander("How does PortfolioAI work?"):

    st.write("""
PortfolioAI extracts information from your resume using AI,
converts it into structured JSON,
and generates a professional portfolio website automatically.
""")

with st.expander("Which resume formats are supported?"):

    st.write("""
• PDF

• DOCX
""")

with st.expander("Can I deploy my portfolio?"):

    st.write("""
Yes.

The generated HTML can be deployed on:

• GitHub Pages

• Netlify

• Vercel

• Firebase Hosting
""")

with st.expander("Which AI model is used?"):

    st.write("""
Current Version

• Groq API

• Llama 3.3 70B Versatile
""")

# ==========================================================
# ABOUT PROJECT
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

with st.expander("ℹ About PortfolioAI", expanded=False):

    st.markdown("""
# 🚀 PortfolioAI

PortfolioAI is an AI-powered application that converts a resume
into a beautiful portfolio website automatically.

---

### Features

- 📄 Resume Parsing

- 🤖 AI Portfolio Generation

- 👀 Live Portfolio Preview

- 📊 Portfolio Analytics

- 📝 Resume Review

- ✨ Resume Improvement

- 💌 Cover Letter Generation

- 📥 HTML Export

- 🤖 JSON Export

---

### Tech Stack

- Python

- Streamlit

- Groq API

- Llama 3.3 70B

- Jinja2

- HTML

- CSS

- JavaScript
""")

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.info("""
🚀 PortfolioAI Version : 1.0

Made with ❤️ using

• Python

• Streamlit

• Groq AI

• HTML

• CSS

• Jinja2
""")

# ==========================================================
# RESET APPLICATION
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

st.header("⚙ Application Controls")

c1, c2 = st.columns(2)

with c1:

    if st.button(
        "🔄 Generate New Portfolio",
        use_container_width=True
    ):

        keys = [
            "resume_text",
            "portfolio_data",
            "portfolio_file",
            "resume_review",
            "improved_resume",
            "cover_letter",
            "generated",
            "error",
        ]

        for key in keys:

            if key in st.session_state:

                del st.session_state[key]

        st.success("Application Reset Successfully.")

        st.rerun()

with c2:

    if st.session_state.generated:

        st.success("✅ Portfolio Ready")

    else:

        st.info("Waiting for Resume Upload")

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

st.header("🖥 System Status")

s1, s2, s3, s4 = st.columns(4)

with s1:

    st.metric(
        "AI Model",
        "Llama 3.3"
    )

with s2:

    st.metric(
        "Framework",
        "Streamlit"
    )

with s3:

    st.metric(
        "Version",
        "v1.0"
    )

with s4:

    st.metric(
        "Status",
        "Online"
    )

# ==========================================================
# DEVELOPER INFORMATION
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

st.header("👩‍💻 Developer")

st.success("""
**PortfolioAI**

Created using

• Python

• Streamlit

• Groq API

• Llama 3.3 70B

• HTML

• CSS

• Jinja2

Designed to automatically convert resumes into modern portfolio websites.
""")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

footer()
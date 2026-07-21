import os
import json
import webbrowser

import streamlit as st
import streamlit.components.v1 as components

from parser import extract_text

from ai import (
    generate_portfolio_json,
    review_resume,
    improve_resume,
    generate_cover_letter,
    generate_interview_questions,
    get_github_profile,
    get_leetcode_profile
)

from generator import (
    generate_portfolio,
    generate_zip,
    generate_pdf,
    export_github_pages,
    export_netlify
)

from styles import load_css

from components import (
    hero,
    stats,
    feature_cards,
    footer
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="PortfolioAI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# LOAD CSS
# ==========================================================

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# ==========================================================
# DEFAULT SESSION STATE
# ==========================================================

DEFAULT_STATE = {

    "resume_text": "",

    "portfolio_data": None,

    "portfolio_file": None,

    "generated": False,

    "theme": "Modern",

    "color": "#38bdf8",

    "font": "Poppins",

    "profile_image": None,

    "github_username": "",

    "leetcode_username": "",

    "github_data": None,

    "leetcode_data": None,

    "resume_review": "",

    "resume_improved": "",

    "cover_letter": "",

    "interview_questions": "",

    "zip_file": None,

    "pdf_file": None,

    "error": None

}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================================
# HEADER
# ==========================================================

hero()

stats()

st.markdown("<br>", unsafe_allow_html=True)

feature_cards()

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# MAIN LAYOUT
# ==========================================================

left, right = st.columns([1, 1.25], gap="large")

# ==========================================================
# LEFT PANEL
# ==========================================================

with left:

    st.markdown("## 📄 Upload Resume")

    st.caption(
        "Upload your resume and let AI build your complete portfolio."
    )

    uploaded_file = st.file_uploader(
        "Resume",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # PROFILE IMAGE
    # ------------------------------------------------------

    st.markdown("### 🖼 Profile Image")

    profile_image = st.file_uploader(
        "Profile Image",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    if profile_image is not None:

        st.session_state.profile_image = profile_image

        st.image(
            profile_image,
            width=180
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # THEME
    # ------------------------------------------------------

    st.markdown("### 🎨 Portfolio Theme")

    theme = st.selectbox(

        "",

        [

            "Modern",

            "Dark",

            "Glass",

            "Minimal",

            "Cyberpunk"

        ],

        index=0,

        label_visibility="collapsed"

    )

    st.session_state.theme = theme

    theme_info = {

        "Modern":
        "✨ Professional and recruiter friendly.",

        "Dark":
        "🌙 Developer inspired portfolio.",

        "Glass":
        "💎 Premium glassmorphism UI.",

        "Minimal":
        "📄 Clean and elegant design.",

        "Cyberpunk":
        "🚀 Futuristic neon theme."

    }

    st.info(theme_info[theme])

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # COLOR
    # ------------------------------------------------------

    st.markdown("### 🎨 Accent Color")

    color = st.color_picker(

        "",

        value=st.session_state.color,

        label_visibility="collapsed"

    )

    st.session_state.color = color

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # FONT
    # ------------------------------------------------------

    st.markdown("### 🔤 Font")

    font = st.selectbox(

        "",

        [

            "Poppins",

            "Inter",

            "Roboto",

            "Montserrat",

            "Open Sans"

        ],

        label_visibility="collapsed"

    )

    st.session_state.font = font

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # GITHUB
    # ------------------------------------------------------

    st.markdown("### 🐙 GitHub Username")

    github_username = st.text_input(

        "",

        placeholder="e.g. sanskriti050",

        label_visibility="collapsed",
        key="github_username"

    )

    # ------------------------------------------------------
    # LEETCODE
    # ------------------------------------------------------

    st.markdown("### 🏆 LeetCode Username")

    leetcode_username = st.text_input(

        "",

        placeholder="e.g. sanskriti050",

        label_visibility="collapsed",
         key="leetcode_username"

    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # AI STATUS
    # ------------------------------------------------------

    st.markdown("### 🤖 AI Status")

    if st.session_state.generated:

        st.success("✅ Portfolio Generated Successfully")

    else:

        st.warning("Waiting for Resume Upload")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # GENERATE BUTTON
    # ------------------------------------------------------

    generate = st.button(

        "🚀 Generate Portfolio",

        use_container_width=True

    )
    # ==========================================================
# RIGHT PANEL
# ==========================================================

with right:

    st.markdown("## 👀 Live Portfolio Preview")

    st.caption(
        "Preview your AI generated portfolio before downloading."
    )

    # ------------------------------------------------------
    # THEME BADGE
    # ------------------------------------------------------

    col1, col2 = st.columns([1, 1])

    with col1:

        st.success(f"🎨 Theme : {st.session_state.theme}")

    with col2:

        st.info(f"🔤 Font : {st.session_state.font}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # COLOR PREVIEW
    # ------------------------------------------------------

    st.markdown("### Selected Accent Color")

    st.markdown(
        f"""
        <div style="
            width:100%;
            height:35px;
            border-radius:12px;
            background:{st.session_state.color};
            border:2px solid white;
        ">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------
    # LIVE PORTFOLIO
    # ------------------------------------------------------

    if st.session_state.generated and st.session_state.portfolio_file:

        try:

            with open(
                st.session_state.portfolio_file,
                "r",
                encoding="utf-8"
            ) as f:

                html = f.read()

            components.html(

                html,

                height=850,

                scrolling=True

            )

        except Exception as e:

            st.error(
                f"Unable to load preview.\n\n{e}"
            )

    else:

        st.info(
            "Generate your portfolio to view the live preview."
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            ### 🚀 Portfolio Preview

            Your generated website will include:

            ✅ Hero Section

            ✅ About

            ✅ Skills

            ✅ Projects

            ✅ Experience

            ✅ Education

            ✅ Certifications

            ✅ GitHub Profile

            ✅ LeetCode Profile

            ✅ Contact Section

            ✅ Responsive Design

            ✅ Selected Theme

            """
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.image(

            "https://placehold.co/1200x700/0f172a/ffffff?text=Portfolio+Preview",

            use_container_width=True

        )
    # ==========================================================
# GENERATE PORTFOLIO
# ==========================================================

if generate:

    st.session_state.error = None

    if uploaded_file is None:

        st.warning("⚠ Please upload your resume first.")

    else:

        try:

            progress = st.progress(0)

            status = st.empty()

            # --------------------------------------------------
            # STEP 1 : READ RESUME
            # --------------------------------------------------

            status.info("📄 Reading Resume...")

            resume_text = extract_text(uploaded_file)

            st.session_state.resume_text = resume_text

            progress.progress(10)

            # --------------------------------------------------
            # STEP 2 : AI PORTFOLIO JSON
            # --------------------------------------------------

            status.info("🤖 Extracting Resume Information...")

            portfolio_data = generate_portfolio_json(
                resume_text
            )

            st.session_state.portfolio_data = portfolio_data

            progress.progress(25)

            # --------------------------------------------------
            # STEP 3 : RESUME REVIEW
            # --------------------------------------------------

            status.info("📝 Reviewing Resume...")

            review = review_resume(
                resume_text
            )

            st.session_state.resume_review = review

            progress.progress(40)

            # --------------------------------------------------
            # STEP 4 : IMPROVE RESUME
            # --------------------------------------------------

            status.info("✨ Improving Resume...")

            improved_resume = improve_resume(
                resume_text
            )

            st.session_state.resume_improved = improved_resume

            progress.progress(55)

            # --------------------------------------------------
            # STEP 5 : COVER LETTER
            # --------------------------------------------------

            status.info("📄 Generating Cover Letter...")

            cover_letter = generate_cover_letter(
                resume_text
            )

            st.session_state.cover_letter = cover_letter

            progress.progress(70)

            # --------------------------------------------------
            # STEP 6 : INTERVIEW QUESTIONS
            # --------------------------------------------------

            status.info("🎯 Preparing Interview Questions...")

            interview_questions = generate_interview_questions(
                resume_text
            )

            st.session_state.interview_questions = (
                interview_questions
            )

            progress.progress(80)

            # --------------------------------------------------
            # STEP 7 : GITHUB PROFILE
            # --------------------------------------------------

            if st.session_state.github_username.strip():

                status.info("🐙 Fetching GitHub Profile...")

                github_data = get_github_profile(
                    st.session_state.github_username
                )

                st.session_state.github_data = github_data

            progress.progress(90)

            # --------------------------------------------------
            # STEP 8 : LEETCODE PROFILE
            # --------------------------------------------------

            if st.session_state.leetcode_username.strip():

                status.info("🏆 Fetching LeetCode Profile...")

                leetcode_data = get_leetcode_profile(
                    st.session_state.leetcode_username
                )

                st.session_state.leetcode_data = (
                    leetcode_data
                )

            progress.progress(95)
                # --------------------------------------------------
            # STEP 9 : GENERATE PORTFOLIO WEBSITE
            # --------------------------------------------------

            status.info("🎨 Building Portfolio Website...")

            portfolio_file = generate_portfolio(

                portfolio_data=portfolio_data,

                theme=st.session_state.theme,

                color=st.session_state.color,

                font=st.session_state.font,

                profile_image=st.session_state.profile_image,

                github_data=st.session_state.github_data,

                leetcode_data=st.session_state.leetcode_data

            )

            st.session_state.portfolio_file = portfolio_file

            progress.progress(97)

            # --------------------------------------------------
            # STEP 10 : GENERATE ZIP
            # --------------------------------------------------

            status.info("📦 Creating ZIP Package...")

            zip_file = generate_zip(

                portfolio_file,

                portfolio_data,

                st.session_state.profile_image

            )

            st.session_state.zip_file = zip_file

            progress.progress(98)

            # --------------------------------------------------
            # STEP 11 : GENERATE PDF
            # --------------------------------------------------

            status.info("📄 Creating Portfolio PDF...")

            pdf_file = generate_pdf(

                portfolio_file

            )

            st.session_state.pdf_file = pdf_file

            progress.progress(99)

            # --------------------------------------------------
            # STEP 12 : EXPORT PROJECT
            # --------------------------------------------------

            status.info("🚀 Preparing Deployment Files...")

            export_github_pages(portfolio_file)

            export_netlify(portfolio_file)

            progress.progress(100)

            # --------------------------------------------------
            # FINISHED
            # --------------------------------------------------

            st.session_state.generated = True

            status.success(
                "🎉 Portfolio Generated Successfully!"
            )

            st.balloons()

            st.success(
                "Everything is ready!"
            )

            st.rerun()

        except Exception as e:

            st.session_state.generated = False

            st.session_state.error = str(e)

            st.error(
                f"❌ {str(e)}"
            )
    # ==========================================================
# AI DASHBOARD
# ==========================================================

if st.session_state.generated:

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    st.header("📊 AI Analysis Dashboard")

    tabs = st.tabs([
        "📄 Resume",
        "🤖 Portfolio JSON",
        "📈 Summary",
        "📝 Resume Review",
        "✨ Improved Resume",
        "📄 Cover Letter",
        "🎯 Interview Questions",
        "🐙 GitHub",
        "🏆 LeetCode"
    ])

    # =====================================================
    # TAB 1 : RESUME
    # =====================================================

    with tabs[0]:

        st.subheader("Extracted Resume")

        st.text_area(
            "",
            st.session_state.resume_text,
            height=450
        )

    # =====================================================
    # TAB 2 : JSON
    # =====================================================

    with tabs[1]:

        st.subheader("Portfolio JSON")

        st.json(
            st.session_state.portfolio_data
        )

    # =====================================================
    # TAB 3 : SUMMARY
    # =====================================================

    with tabs[2]:

        data = st.session_state.portfolio_data

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Skills",
            len(data.get("skills", []))
        )

        col2.metric(
            "Projects",
            len(data.get("projects", []))
        )

        col3.metric(
            "Experience",
            len(data.get("experience", []))
        )

        col4.metric(
            "Certificates",
            len(data.get("certifications", []))
        )

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### 👤 Basic Details")

            st.write(
                "**Name:**",
                data.get("name", "-")
            )

            st.write(
                "**Headline:**",
                data.get("headline", "-")
            )

            st.write(
                "**Email:**",
                data.get("email", "-")
            )

        with c2:

            st.markdown("### 📞 Contact")

            st.write(
                "**Phone:**",
                data.get("phone", "-")
            )

            st.write(
                "**GitHub:**",
                data.get("github", "-")
            )

            st.write(
                "**LinkedIn:**",
                data.get("linkedin", "-")
            )

    # =====================================================
    # TAB 4 : REVIEW
    # =====================================================

    with tabs[3]:

        st.subheader("AI Resume Review")

        st.markdown(
            st.session_state.resume_review
        )

    # =====================================================
    # TAB 5 : IMPROVED RESUME
    # =====================================================

    with tabs[4]:

        st.subheader("Improved Resume")

        st.text_area(

            "",

            st.session_state.resume_improved,

            height=500

        )

    # =====================================================
    # TAB 6 : COVER LETTER
    # =====================================================

    with tabs[5]:

        st.subheader("Cover Letter")

        st.text_area(

            "",

            st.session_state.cover_letter,

            height=500

        )

    # =====================================================
    # TAB 7 : INTERVIEW QUESTIONS
    # =====================================================

    with tabs[6]:

        st.subheader("Interview Questions")

        st.markdown(

            st.session_state.interview_questions

        )

    # =====================================================
    # TAB 8 : GITHUB
    # =====================================================

    with tabs[7]:

        st.subheader("GitHub Profile")

        github = st.session_state.github_data

        if github:

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Followers",
                github.get("followers", 0)
            )

            c2.metric(
                "Following",
                github.get("following", 0)
            )

            c3.metric(
                "Repositories",
                github.get("public_repos", 0)
            )

            st.write(
                "**Profile:**",
                github.get("html_url", "-")
            )

        else:

            st.info(
                "GitHub username not provided."
            )

    # =====================================================
    # TAB 9 : LEETCODE
    # =====================================================

    with tabs[8]:

        st.subheader("LeetCode Profile")

        lc = st.session_state.leetcode_data

        if lc:

            c1, c2 = st.columns(2)

            c1.metric(
                "Solved",
                lc.get("solved", 0)
            )

            c2.metric(
                "Ranking",
                lc.get("ranking", "-")
            )

            st.write(
                "**Profile:**",
                lc.get("profile", "-")
            )

        else:

            st.info(
                "LeetCode username not provided."
            )
    # ==========================================================
# DOWNLOAD & EXPORT CENTER
# ==========================================================

if st.session_state.generated:

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    st.header("📥 Download & Export Portfolio")

    download_tab, deploy_tab = st.tabs(
        [
            "📥 Downloads",
            "🚀 Deployment"
        ]
    )

    # ======================================================
    # DOWNLOAD TAB
    # ======================================================

    with download_tab:

        d1, d2 = st.columns(2)

        # ---------------------------------------------
        # LEFT COLUMN
        # ---------------------------------------------

        with d1:

            st.subheader("Portfolio Files")

            # HTML

            if st.session_state.portfolio_file:

                with open(
                    st.session_state.portfolio_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    html = f.read()

                st.download_button(

                    "🌐 Download HTML",

                    data=html,

                    file_name="portfolio.html",

                    mime="text/html",

                    use_container_width=True

                )

            # JSON

            st.download_button(

                "🤖 Download JSON",

                data=json.dumps(

                    st.session_state.portfolio_data,

                    indent=4

                ),

                file_name="portfolio.json",

                mime="application/json",

                use_container_width=True

            )

            # Resume Text

            st.download_button(

                "📄 Download Resume Text",

                data=st.session_state.resume_text,

                file_name="resume.txt",

                mime="text/plain",

                use_container_width=True

            )

        # ---------------------------------------------
        # RIGHT COLUMN
        # ---------------------------------------------

        with d2:

            st.subheader("Generated Files")

            # ZIP

            if st.session_state.zip_file:

                with open(
                    st.session_state.zip_file,
                    "rb"
                ) as f:

                    st.download_button(

                        "📦 Download ZIP",

                        data=f,

                        file_name="PortfolioAI.zip",

                        mime="application/zip",

                        use_container_width=True

                    )

            # PDF

            if st.session_state.pdf_file:

                with open(
                    st.session_state.pdf_file,
                    "rb"
                ) as f:

                    st.download_button(

                        "📄 Download PDF",

                        data=f,

                        file_name="Portfolio.pdf",

                        mime="application/pdf",

                        use_container_width=True

                    )

            # Open Portfolio

            if st.button(

                "🌍 Open Portfolio",

                use_container_width=True

            ):

                webbrowser.open(

                    "file://" +

                    os.path.abspath(

                        st.session_state.portfolio_file

                    )

                )

                st.success(

                    "Portfolio opened in browser."

                )

    # ======================================================
    # DEPLOYMENT TAB
    # ======================================================

    with deploy_tab:

        st.subheader("Deployment Ready")

        c1, c2 = st.columns(2)

        with c1:

            st.info("""

### GitHub Pages

One-click export

Repository Ready

Deploy Ready

""")

            if st.button(

                "🚀 Export GitHub Pages",

                use_container_width=True

            ):

                export_github_pages(

                    st.session_state.portfolio_file

                )

                st.success(

                    "GitHub Pages files created."

                )

        with c2:

            st.info("""

### Netlify

Drag & Drop Ready

Production Ready

""")

            if st.button(

                "🌐 Export Netlify",

                use_container_width=True

            ):

                export_netlify(

                    st.session_state.portfolio_file

                )

                st.success(

                    "Netlify package created."

                )

    st.success(

        "✅ Portfolio is ready for deployment."

    )
    # ==========================================================
# ERROR PANEL
# ==========================================================

if st.session_state.error:

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    st.error("❌ Something went wrong while generating the portfolio.")

    with st.expander("Show Error Details"):

        st.code(
            st.session_state.error,
            language="text"
        )

# ==========================================================
# QUICK TIPS
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

st.header("💡 Tips for Best Results")

left_tip, right_tip = st.columns(2)

with left_tip:

    st.success("""

### Resume Tips

✔ ATS Friendly Resume

✔ Mention GitHub

✔ Mention LinkedIn

✔ Add Projects

✔ Add Skills

✔ Add Internship

✔ Use Action Verbs

✔ Keep Resume Updated

""")

with right_tip:

    st.info("""

### Portfolio Tips

🚀 Upload Professional Photo

🚀 Choose Theme Carefully

🚀 Add GitHub Username

🚀 Add LeetCode Username

🚀 Download ZIP

🚀 Deploy on GitHub Pages

🚀 Deploy on Netlify

""")

# ==========================================================
# PROJECT STATISTICS
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

st.header("📈 Portfolio Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Themes",
    "5"
)

c2.metric(
    "Export Formats",
    "5"
)

c3.metric(
    "AI Features",
    "6"
)

c4.metric(
    "Deployment",
    "2"
)

# ==========================================================
# FEATURE CHECKLIST
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

st.header("✅ Features Included")

st.markdown("""

### AI

- ✅ Resume Parser
- ✅ Portfolio JSON Generator
- ✅ Resume Review
- ✅ Resume Improver
- ✅ Cover Letter Generator
- ✅ Interview Question Generator

---

### Portfolio

- ✅ HTML Portfolio
- ✅ Live Preview
- ✅ Multiple Themes
- ✅ Color Customization
- ✅ Font Customization
- ✅ Profile Image Upload

---

### Integrations

- ✅ GitHub Profile
- ✅ LeetCode Profile

---

### Export

- ✅ HTML
- ✅ JSON
- ✅ ZIP
- ✅ PDF

---

### Deployment

- ✅ GitHub Pages
- ✅ Netlify Ready

""")

# ==========================================================
# ABOUT
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

with st.expander("ℹ About PortfolioAI"):

    st.markdown("""

# 🚀 PortfolioAI v2.0

PortfolioAI is an AI-powered portfolio generator.

It converts a resume into a beautiful developer portfolio.

---

## Features

- Resume Parsing

- AI Portfolio Generator

- Resume Review

- Resume Improvement

- Cover Letter

- Interview Questions

- Live Portfolio Preview

- Profile Image Support

- Multiple Themes

- GitHub Integration

- LeetCode Integration

- ZIP Export

- PDF Export

- GitHub Pages Export

- Netlify Export

---

## Tech Stack

- Python

- Streamlit

- Groq API

- Jinja2

- HTML

- CSS

- JavaScript

""")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

footer()
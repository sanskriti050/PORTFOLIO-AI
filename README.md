# 🚀 PortfolioAI — AI Powered Resume to Portfolio Generator

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<img src="https://img.shields.io/badge/Groq-LLM-00C853?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Jinja2-Template-B41717?style=for-the-badge"/>

<img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge"/>

</p>

---

## 🌟 Overview

**PortfolioAI** is an AI-powered web application that transforms a resume into a beautiful, modern, and responsive portfolio website in just a few seconds.

Instead of manually designing a portfolio, users simply upload their resume, and PortfolioAI uses an LLM to extract structured information, generate professional content, and build a complete portfolio website automatically.

The application also includes multiple AI-powered career tools such as resume analysis, resume improvement, cover letter generation, interview question generation, and export utilities.

---

# ✨ Features

### 🤖 AI Features

* AI Resume Parsing
* AI Portfolio JSON Generation
* AI Resume Review
* AI Resume Improvement
* AI Cover Letter Generator
* AI Interview Questions Generator

---

### 🌐 Portfolio Generator

* Professional Portfolio Website
* Responsive Design
* Live Portfolio Preview
* HTML Portfolio Export
* JSON Export
* ZIP Export
* PDF Export

---

### 🎨 Customization

* Portfolio Theme Selection
* Accent Color Selection
* Font Selection
* Profile Image Upload *(In Progress)*

---

### 🚀 Deployment

* GitHub Pages Export
* Netlify Export

---

### 📊 Dashboard

* Resume Preview
* Portfolio JSON Viewer
* AI Summary
* Portfolio Statistics

---

# 🖼 Application Workflow

```
Resume Upload
        │
        ▼
Resume Parsing
        │
        ▼
Groq AI Analysis
        │
        ▼
Portfolio JSON
        │
        ▼
Portfolio Website
        │
        ▼
Preview + Download + Export
```

---

# 🛠 Tech Stack

## Frontend

* Streamlit
* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

---

## Backend

* Python
* Streamlit
* Jinja2

---

## AI

* Groq API
* Llama 3.3 70B Versatile

---

## Libraries

* streamlit
* groq
* python-dotenv
* Jinja2
* ReportLab
* requests
* python-docx
* PyPDF2

---

# 📁 Project Structure

```
PortfolioAI/

│
├── app.py
├── ai.py
├── parser.py
├── generator.py
├── styles.py
├── components.py
│
├── templates/
│     └── portfolio.html
│
├── themes/
│     ├── modern.css
│     ├── dark.css
│     ├── glass.css
│     ├── minimal.css
│     └── cyberpunk.css
│
├── generated/
│
├── assets/
│
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/PortfolioAI.git

cd PortfolioAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a **.env** file

```env
GROQ_API_KEY=your_groq_api_key
```

Run the application

```bash
streamlit run app.py
```

---

# 📄 How to Use

1. Upload Resume (PDF/DOCX)
2. Select Portfolio Theme
3. Choose Accent Color
4. Choose Font
5. Enter GitHub Username *(optional)*
6. Enter LeetCode Username *(optional)*
7. Click **Generate Portfolio**
8. Preview Portfolio
9. Download HTML / JSON / ZIP / PDF
10. Deploy using GitHub Pages or Netlify

---

# 📦 Export Options

* HTML Portfolio
* Portfolio JSON
* ZIP Package
* PDF Portfolio
* GitHub Pages Folder
* Netlify Folder

---

# 📸 Screenshots

Add screenshots here after deployment.

Example:

```
Home Screen

Upload Resume

Portfolio Preview

AI Dashboard

Generated Portfolio

Export Section
```

---

# 🚀 Future Enhancements

* Real Multiple Themes
* GitHub Statistics Integration
* LeetCode Statistics Integration
* Theme Switching Inside Portfolio
* Portfolio Chatbot
* AI Job Match Score
* Resume vs Portfolio Comparison
* Portfolio Analytics
* Contact Form Integration
* SEO Optimization
* One-Click Deployment
* Vercel Export

---

# 🎯 Why PortfolioAI?

✔ Converts resumes into professional portfolio websites

✔ Uses LLMs for intelligent content generation

✔ Eliminates manual portfolio building

✔ Includes multiple AI career tools

✔ Export-ready for deployment

✔ Beginner-friendly interface

---

# 💡 Learning Outcomes

This project demonstrates practical experience with:

* Large Language Models (LLMs)
* Prompt Engineering
* Resume Parsing
* AI Content Generation
* Jinja2 Templating
* Streamlit Application Development
* JSON Processing
* File Handling
* PDF Generation
* ZIP Packaging
* Responsive Web Design
* Deployment Workflows

---

# 👨‍💻 Author

**Sanskriti Agarwal**

B.Tech – Artificial Intelligence & Machine Learning

GLA University, Mathura

GitHub: https://github.com/sanskriti050

---

# 📜 License

This project is licensed under the **MIT License**.

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future improvements.

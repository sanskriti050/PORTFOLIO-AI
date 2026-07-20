import streamlit as st


# =====================================================
# HERO SECTION
# =====================================================

def hero():
    st.markdown(
        """
        <div class="hero">
            <h1>🚀 PortfolioAI</h1>
            <p>
                Transform Your Resume Into a Stunning Developer Portfolio Website Using AI
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# STATS
# =====================================================

def stats():

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="⭐ ATS Ready",
            value="98%",
            delta="Professional"
        )

    with col2:
        st.metric(
            label="💻 Skills",
            value="25+",
            delta="Detected"
        )

    with col3:
        st.metric(
            label="📂 Projects",
            value="6+",
            delta="Portfolio Ready"
        )

    with col4:
        st.metric(
            label="⚡ AI Time",
            value="30 sec",
            delta="Average"
        )


# =====================================================
# SECTION TITLE
# =====================================================

def section_title(title, subtitle=""):

    st.markdown(
        f"""
        <div style="margin-top:25px;margin-bottom:15px;">

            <h2 style="color:white;">
                {title}
            </h2>

            <p style="color:#cbd5e1;">
                {subtitle}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# FEATURES
# =====================================================

def feature_cards():

    st.markdown("## ✨ Why PortfolioAI?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            "📄 **Resume Upload**\n\nUpload your PDF or DOCX resume."
        )

    with c2:
        st.info(
            "🤖 **AI Portfolio Generation**\n\nGenerate a beautiful developer portfolio."
        )

    with c3:
        st.info(
            "🚀 **One Click Download**\n\nDownload your complete portfolio website."
        )


# =====================================================
# FOOTER
# =====================================================

def footer():
    st.divider()

    st.markdown(
        """
        <p style="text-align:center; color:#94a3b8; font-size:14px;">
            🚀 <b>PortfolioAI</b><br>
            Built with ❤️ using Streamlit • Python • Gemini AI
        </p>
        """,
        unsafe_allow_html=True,
    )
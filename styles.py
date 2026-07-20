def load_css():
    return """
<style>

/* =====================================================
   GOOGLE FONT
===================================================== */

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html,
body,
[class*="css"]{
    font-family:'Poppins',sans-serif;
}

/* =====================================================
   BACKGROUND
===================================================== */

.stApp{

    background:linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827,
        #1e293b
    );

    background-size:400% 400%;

    animation:bgAnimation 18s ease infinite;

    color:white;

}

@keyframes bgAnimation{

    0%{
        background-position:0% 50%;
    }

    50%{
        background-position:100% 50%;
    }

    100%{
        background-position:0% 50%;
    }

}

/* =====================================================
   HIDE STREAMLIT
===================================================== */

#MainMenu,
header,
footer{
    visibility:hidden;
}

[data-testid="stToolbar"]{
    display:none;
}

/* =====================================================
   HERO
===================================================== */

.hero{

    text-align:center;

    padding:65px 40px;

    margin-bottom:35px;

    border-radius:25px;

    background:rgba(255,255,255,.06);

    border:1px solid rgba(255,255,255,.12);

    backdrop-filter:blur(18px);

    box-shadow:0 12px 45px rgba(0,0,0,.35);

}

.hero h1{

    font-size:62px;

    font-weight:800;

    margin-bottom:15px;

    background:linear-gradient(
        90deg,
        #38bdf8,
        #818cf8,
        #ec4899,
        #38bdf8
    );

    background-size:300%;

    -webkit-background-clip:text;

    color:transparent;

    animation:gradientText 8s linear infinite;

}

@keyframes gradientText{

    from{
        background-position:0%;
    }

    to{
        background-position:300%;
    }

}

.hero p{

    font-size:22px;

    color:#cbd5e1;

}

/* =====================================================
   GLASS CARD
===================================================== */

.card{

    background:rgba(255,255,255,.07);

    padding:25px;

    border-radius:22px;

    border:1px solid rgba(255,255,255,.12);

    backdrop-filter:blur(18px);

    box-shadow:0 8px 30px rgba(0,0,0,.25);

    transition:all .35s ease;

}

.card:hover{

    transform:translateY(-8px);

    box-shadow:0 0 35px rgba(56,189,248,.35);

}

.card h1,
.card h2,
.card h3,
.card h4,
.card h5,
.card p{

    color:white;

}

/* =====================================================
   METRIC CARDS
===================================================== */

[data-testid="metric-container"]{

    background:rgba(255,255,255,.07);

    border-radius:18px;

    padding:15px;

    border:1px solid rgba(255,255,255,.08);

    box-shadow:0 5px 20px rgba(0,0,0,.2);

    transition:all .3s ease;

}

[data-testid="metric-container"]:hover{

    transform:translateY(-5px);

    box-shadow:0 0 25px rgba(56,189,248,.45);

}

/* =====================================================
   BUTTON
===================================================== */

.stButton>button{

    width:100%;

    height:55px;

    border:none;

    border-radius:14px;

    font-size:18px;

    font-weight:600;

    color:white;

    cursor:pointer;

    background:linear-gradient(
        90deg,
        #06b6d4,
        #6366f1,
        #ec4899
    );

    background-size:300%;

    transition:all .35s ease;

}

.stButton>button:hover{

    background-position:right center;

    transform:scale(1.03);

    box-shadow:0 0 25px rgba(99,102,241,.5);

}

/* =====================================================
   FILE UPLOADER
===================================================== */

[data-testid="stFileUploader"]{

    background:rgba(255,255,255,.06);

    padding:20px;

    border-radius:18px;

    border:2px dashed rgba(56,189,248,.45);

    transition:all .3s ease;

}

[data-testid="stFileUploader"]:hover{

    border-color:#818cf8;

    box-shadow:0 0 25px rgba(99,102,241,.35);

}

[data-testid="stFileUploader"] label{

    font-size:18px;

    font-weight:600;

}

/* =====================================================
   SELECTBOX
===================================================== */

[data-baseweb="select"]{

    border-radius:12px;

}

div[data-baseweb="select"]>div{

    background:#1e293b !important;

    color:white !important;

    border-radius:12px;

    border:1px solid rgba(255,255,255,.1);

}

/* =====================================================
   TEXT AREA
===================================================== */

textarea{

    background:#0f172a !important;

    color:white !important;

    border-radius:15px !important;

    border:1px solid #334155 !important;

}

/* =====================================================
   INFO / SUCCESS / WARNING
===================================================== */

[data-testid="stAlert"]{

    border-radius:15px;

}

/* =====================================================
   PROGRESS BAR
===================================================== */

[data-testid="stProgressBar"]{

    border-radius:10px;

}

/* =====================================================
   SCROLLBAR
===================================================== */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-track{

    background:#0f172a;

}

::-webkit-scrollbar-thumb{

    background:#38bdf8;

    border-radius:10px;

}

::-webkit-scrollbar-thumb:hover{

    background:#60a5fa;

}

/* =====================================================
   LINKS
===================================================== */

a{

    color:#38bdf8;

}

a:hover{

    color:#818cf8;

}

</style>
"""
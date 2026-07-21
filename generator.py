import os
import shutil
import zipfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).parent

TEMPLATE_DIR = BASE_DIR / "templates"

GENERATED_DIR = BASE_DIR / "generated"

ASSETS_DIR = GENERATED_DIR / "assets"

THEMES_DIR = BASE_DIR / "themes"

# Create folders if not present
GENERATED_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# ==========================================================
# JINJA ENVIRONMENT
# ==========================================================

env = Environment(

    loader=FileSystemLoader(str(TEMPLATE_DIR)),

    autoescape=True

)

# ==========================================================
# AVAILABLE THEMES
# ==========================================================

THEMES = {

    "Modern": "modern.css",

    "Glass": "glass.css",

    "Dark": "dark.css",

    "Minimal": "minimal.css",

    "Cyberpunk": "cyberpunk.css"

}

# ==========================================================
# LOAD THEME CSS
# ==========================================================

def load_theme(theme):

    css_file = THEMES.get(

        theme,

        "modern.css"

    )

    css_path = THEMES_DIR / css_file

    if css_path.exists():

        with open(

            css_path,

            "r",

            encoding="utf-8"

        ) as f:

            return f.read()

    return ""

# ==========================================================
# SAVE PROFILE IMAGE
# ==========================================================

def save_profile_image(image):

    if image is None:

        return None

    extension = image.name.split(".")[-1]

    output = ASSETS_DIR / f"profile.{extension}"

    with open(output, "wb") as f:

        f.write(image.getbuffer())

    return f"assets/profile.{extension}"

# ==========================================================
# COPY STATIC FILES
# ==========================================================

def copy_static_files():

    static_dir = BASE_DIR / "static"

    if not static_dir.exists():

        return

    destination = GENERATED_DIR / "static"

    if destination.exists():

        shutil.rmtree(destination)

    shutil.copytree(

        static_dir,

        destination

    )

# ==========================================================
# DELETE OLD OUTPUT
# ==========================================================

def clean_generated():

    if GENERATED_DIR.exists():

        for item in GENERATED_DIR.iterdir():

            if item.is_file():

                item.unlink()

            elif item.is_dir():

                shutil.rmtree(item)

    GENERATED_DIR.mkdir(exist_ok=True)

    ASSETS_DIR.mkdir(exist_ok=True)
# ==========================================================
# GENERATE PORTFOLIO
# ==========================================================

def generate_portfolio(
    portfolio_data,
    theme="Modern",
    color="#38bdf8",
    font="Poppins",
    profile_image=None,
    github_data=None,
    leetcode_data=None
):

    # ------------------------------------------------------
    # CLEAN OUTPUT
    # ------------------------------------------------------

    clean_generated()

    copy_static_files()

    # ------------------------------------------------------
    # PROFILE IMAGE
    # ------------------------------------------------------

    image_path = save_profile_image(profile_image)

    # ------------------------------------------------------
    # LOAD TEMPLATE
    # ------------------------------------------------------

    template = env.get_template(
        "portfolio.html"
    )

    # ------------------------------------------------------
    # LOAD THEME
    # ------------------------------------------------------

    theme_css = load_theme(theme)

    # ------------------------------------------------------
    # DEFAULT VALUES
    # ------------------------------------------------------

    data = dict(portfolio_data)

    data.setdefault("name", "")
    data.setdefault("headline", "")
    data.setdefault("about", "")
    data.setdefault("skills", [])
    data.setdefault("projects", [])
    data.setdefault("education", [])
    data.setdefault("experience", [])
    data.setdefault("certifications", [])
    data.setdefault("github", "")
    data.setdefault("linkedin", "")
    data.setdefault("email", "")
    data.setdefault("phone", "")

    # ------------------------------------------------------
    # EXTRA DATA
    # ------------------------------------------------------

    data["theme"] = theme

    data["theme_css"] = theme_css

    data["accent_color"] = color

    data["font"] = font

    data["profile_image"] = image_path

    data["github_data"] = github_data

    data["leetcode_data"] = leetcode_data

    # ------------------------------------------------------
    # RENDER HTML
    # ------------------------------------------------------

    html = template.render(**data)

    # ------------------------------------------------------
    # OUTPUT FILE
    # ------------------------------------------------------

    output_file = GENERATED_DIR / "index.html"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    return str(output_file)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


# ==========================================================
# GENERATE ZIP
# ==========================================================

def generate_zip(

    portfolio_file,

    portfolio_data,

    profile_image=None

):

    zip_path = GENERATED_DIR / "PortfolioAI.zip"

    with zipfile.ZipFile(

        zip_path,

        "w",

        zipfile.ZIP_DEFLATED

    ) as zipf:

        # -------------------------
        # HTML
        # -------------------------

        if os.path.exists(portfolio_file):

            zipf.write(

                portfolio_file,

                arcname="index.html"

            )

        # -------------------------
        # Assets
        # -------------------------

        assets = GENERATED_DIR / "assets"

        if assets.exists():

            for file in assets.rglob("*"):

                if file.is_file():

                    zipf.write(

                        file,

                        arcname=str(

                            file.relative_to(GENERATED_DIR)

                        )

                    )

        # -------------------------
        # Portfolio JSON
        # -------------------------

        json_file = GENERATED_DIR / "portfolio_data.json"

        with open(

            json_file,

            "w",

            encoding="utf-8"

        ) as f:

            import json

            json.dump(

                portfolio_data,

                f,

                indent=4,

                ensure_ascii=False

            )

        zipf.write(

            json_file,

            arcname="portfolio_data.json"

        )

    return str(zip_path)


# ==========================================================
# GENERATE PDF
# ==========================================================

def generate_pdf(portfolio_file):

    pdf_path = GENERATED_DIR / "Portfolio.pdf"

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(str(pdf_path))

    story = []

    # -------------------------
    # Read HTML
    # -------------------------

    with open(

        portfolio_file,

        "r",

        encoding="utf-8"

    ) as f:

        html = f.read()

    # Very basic HTML cleanup
    import re

    text = re.sub(r"<[^>]+>", "", html)

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]

    # -------------------------
    # Build PDF
    # -------------------------

    for line in lines:

        story.append(

            Paragraph(

                line,

                styles["BodyText"]

            )

        )

    document.build(story)

    return str(pdf_path)

# ==========================================================
# EXPORT FOR GITHUB PAGES
# ==========================================================

def export_github_pages(portfolio_file):

    github_dir = GENERATED_DIR / "github-pages"

    # Delete old export
    if github_dir.exists():

        shutil.rmtree(github_dir)

    github_dir.mkdir(parents=True)

    # --------------------------
    # Copy HTML
    # --------------------------

    shutil.copy(

        portfolio_file,

        github_dir / "index.html"

    )

    # --------------------------
    # Copy Assets
    # --------------------------

    assets = GENERATED_DIR / "assets"

    if assets.exists():

        shutil.copytree(

            assets,

            github_dir / "assets"

        )

    # --------------------------
    # .nojekyll
    # --------------------------

    (github_dir / ".nojekyll").touch()

    return str(github_dir)


# ==========================================================
# EXPORT FOR NETLIFY
# ==========================================================

def export_netlify(portfolio_file):

    netlify_dir = GENERATED_DIR / "netlify"

    # Delete old export
    if netlify_dir.exists():

        shutil.rmtree(netlify_dir)

    netlify_dir.mkdir(parents=True)

    # --------------------------
    # Copy HTML
    # --------------------------

    shutil.copy(

        portfolio_file,

        netlify_dir / "index.html"

    )

    # --------------------------
    # Copy Assets
    # --------------------------

    assets = GENERATED_DIR / "assets"

    if assets.exists():

        shutil.copytree(

            assets,

            netlify_dir / "assets"

        )

    # --------------------------
    # netlify.toml
    # --------------------------

    toml = """
[build]

publish = "."

[[redirects]]

from = "/*"

to = "/index.html"

status = 200
"""

    with open(

        netlify_dir / "netlify.toml",

        "w",

        encoding="utf-8"

    ) as f:

        f.write(toml)

    return str(netlify_dir)


# ==========================================================
# COPY THEME FILES
# ==========================================================

def copy_theme_files():

    css_dir = GENERATED_DIR / "themes"

    css_dir.mkdir(exist_ok=True)

    if THEMES_DIR.exists():

        for file in THEMES_DIR.glob("*.css"):

            shutil.copy(

                file,

                css_dir / file.name

            )


# ==========================================================
# COPY ASSETS
# ==========================================================

def copy_assets():

    source = BASE_DIR / "assets"

    if not source.exists():

        return

    destination = GENERATED_DIR / "assets"

    if destination.exists():

        shutil.rmtree(destination)

    shutil.copytree(

        source,

        destination

    )


# ==========================================================
# PROJECT INFORMATION
# ==========================================================

def project_info():

    return {

        "name": "PortfolioAI",

        "version": "2.0",

        "author": "PortfolioAI",

        "features": [

            "AI Resume Parsing",

            "Portfolio Generator",

            "Multiple Themes",

            "Profile Image",

            "GitHub Integration",

            "LeetCode Integration",

            "PDF Export",

            "ZIP Export",

            "GitHub Pages Export",

            "Netlify Export"

        ]

    }
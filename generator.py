import os
from jinja2 import Environment, FileSystemLoader


# ==========================================================
# CREATE OUTPUT DIRECTORY
# ==========================================================

OUTPUT_DIR = "generated"

if os.path.exists(OUTPUT_DIR):

    if os.path.isfile(OUTPUT_DIR):

        os.remove(OUTPUT_DIR)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ==========================================================
# TEMPLATE ENVIRONMENT
# ==========================================================

env = Environment(

    loader=FileSystemLoader("templates"),

    autoescape=True

)

# ==========================================================
# GENERATE PORTFOLIO
# ==========================================================

def generate_portfolio(data, theme="Modern"):

    """
    Generates HTML portfolio from resume JSON.

    Parameters
    ----------
    data : dict
        Portfolio JSON

    theme : str
        Modern / Dark / Glass / Minimal / Cyberpunk

    Returns
    -------
    str
        generated/index.html
    """

    template = env.get_template(
        "portfolio.html"
    )

    html = template.render(

        **data,

        theme=theme

    )

    output_path = os.path.join(

        OUTPUT_DIR,

        "index.html"

    )

    with open(

        output_path,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(html)

    return output_path


# ==========================================================
# SAVE JSON
# ==========================================================

def save_json(data):

    import json

    json_path = os.path.join(

        OUTPUT_DIR,

        "portfolio.json"

    )

    with open(

        json_path,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )

    return json_path


# ==========================================================
# SAVE RESUME TEXT
# ==========================================================

def save_resume(resume_text):

    resume_path = os.path.join(

        OUTPUT_DIR,

        "resume.txt"

    )

    with open(

        resume_path,

        "w",

        encoding="utf-8"

    ) as f:

        f.write(resume_text)

    return resume_path


# ==========================================================
# EXPORT ALL
# ==========================================================

def export_all(

    data,

    resume_text,

    theme="Modern"

):

    html_file = generate_portfolio(

        data,

        theme

    )

    json_file = save_json(

        data

    )

    resume_file = save_resume(

        resume_text

    )

    return {

        "html": html_file,

        "json": json_file,

        "resume": resume_file

    }
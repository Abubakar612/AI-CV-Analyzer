from flask import Flask, render_template, request
from analyzer import analyze_cv, analyze_recruiter_files
import re

app = Flask(__name__)


def validate_form():
    skills = request.form["skills"].strip()
    experience = request.form["experience"].strip()
    degree = request.form["degree"].strip()
    field = request.form["field"].strip()

    # Skills check
    if skills == "":
        return "Skills cannot be empty."

    if skills.replace(",", "").replace(" ", "").isdigit():
        return "Skills cannot contain numbers only."

    # Allow skills like HTML5, CSS3, C++, C#, Node.js
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    for skill in skill_list:
        if not re.search(r"[a-zA-Z]", skill):
            return "Each skill must contain at least one alphabet."

    # Experience check
    if not experience.isdigit():
        return "Experience must be a number."

    experience_num = int(experience)
    if experience_num < 0 or experience_num > 20:
        return "Experience must be between 0 and 20 years."

    # Degree check
    if degree == "":
        return "Degree cannot be empty."

    if degree.isdigit():
        return "Degree cannot contain numbers only."

    # Field check
    if field == "":
        return "Field cannot be empty."

    if field.isdigit():
        return "Field cannot contain numbers only."

    if re.search(r"\d", field):
        return "Field cannot contain numbers."

    return {
        "skills": skills,
        "experience": experience,
        "degree": degree,
        "field": field
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/applicant", methods=["POST"])
def applicant():
    job = validate_form()

    if isinstance(job, str):
        return job

    cv_file = request.files["cv"]

    result = analyze_cv(cv_file.filename, cv_file.read(), job)

    return render_template("result.html", result=result)


@app.route("/recruiter", methods=["POST"])
def recruiter():
    job = validate_form()

    if isinstance(job, str):
        return job

    files = request.files.getlist("cvs")

    results = analyze_recruiter_files(files, job)

    return render_template("recruiter_result.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)

import io
import re
import zipfile
import pdfplumber
import joblib

model = joblib.load("cv_model.pkl")


def is_valid_cv(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page_count = len(pdf.pages)

    return page_count <= 5, page_count


def extract_text(pdf_bytes):
    text = ""

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            content = page.extract_text()

            if content:
                text += content + " "
            else:
                words = page.extract_words()
                text += " ".join([w.get("text", "") for w in words]) + " "

    text = text.lower()
    text = text.replace(".", " ")
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s*(years|year|yrs|yr)', text)
    return max([int(m[0]) for m in matches]) if matches else 0


def get_degree_level(text):
    text = text.lower()
    text = text.replace(".", " ")
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text)

    if re.search(r"\bphd\b|\bph\s*d\b|doctor of philosophy|doctorate", text):
        return 5

    if (
        re.search(r"\bms\b", text) or
        re.search(r"\bm\s*s\b", text) or
        re.search(r"\bm\s*sc\b", text) or
        re.search(r"\bmsc\b", text) or
        re.search(r"\bmcs\b", text) or
        "master" in text or
        "masters" in text or
        "master of science" in text
    ):
        return 4

    if (
        re.search(r"\bbs\b", text) or
        re.search(r"\bb\s*s\b", text) or
        re.search(r"\bbsc\b", text) or
        re.search(r"\bb\s*sc\b", text) or
        re.search(r"\bbsit\b", text) or
        re.search(r"\bbscs\b", text) or
        "bachelor" in text or
        "bachelors" in text or
        "bachelor of science" in text
    ):
        return 3

    return 0


def degree_label(level):
    if level == 5:
        return "PhD"
    elif level == 4:
        return "MS"
    elif level == 3:
        return "BS"
    else:
        return "Not Found"


degree_map = {
    "cs": ["cs", "computer science"],
    "it": ["it", "information technology"],
    "ai": ["ai", "artificial intelligence"],
    "se": ["se", "software engineering"]
}


def field_match(text, fields):
    text = text.lower()

    for f in fields:
        f = f.strip().lower()

        if f in degree_map:
            for alias in degree_map[f]:
                if alias in text:
                    return True

        if f in text:
            return True

    return False


def required_degree_level(degree):
    degree = degree.lower()
    degree = degree.replace(".", " ")
    degree = degree.replace("-", " ")
    degree = re.sub(r"\s+", " ", degree)

    if "phd" in degree or "doctor" in degree:
        return 5
    elif "ms" in degree or "m s" in degree or "master" in degree:
        return 4
    elif "bs" in degree or "b s" in degree or "bachelor" in degree:
        return 3
    else:
        return 3


def analyze_cv(filename, pdf_bytes, job):
    try:
        valid_cv, page_count = is_valid_cv(pdf_bytes)

        if not valid_cv:
            return {
                "Candidate": filename,
                "Skills": "Skipped",
                "Skill_Percent": 0,
                "Experience": "Skipped",
                "Degree": "Skipped",
                "Required_Degree": "Skipped",
                "Degree_Match": "No",
                "Field_Match": "No",
                "AI_Score": 0,
                "Status": f"Rejected - Not a CV or too long ({page_count} pages)"
            }

        text = extract_text(pdf_bytes)

        req_skills = [s.strip().lower() for s in job["skills"].split(",") if s.strip()]
        matched = [s for s in req_skills if s in text]

        skill_score = len(matched) / len(req_skills) if req_skills else 0

        cv_exp = extract_experience(text)
        req_exp = int(job["experience"])
        exp_score = min(cv_exp / req_exp, 1.0) if req_exp > 0 else 1

        cv_deg = get_degree_level(text)
        req_deg = required_degree_level(job["degree"])

        degree_ok = cv_deg >= req_deg

        fields = job["field"].split(",")
        field_ok = field_match(text, fields)

        if not degree_ok:
            prediction = 0
        else:
            edu_score = 1
            prediction = model.predict([[skill_score, exp_score, edu_score]])[0]

        return {
            "Candidate": filename,
            "Skills": ", ".join(matched) if matched else "None",
            "Skill_Percent": round(skill_score * 100, 2),
            "Experience": cv_exp,
            "Degree": degree_label(cv_deg),
            "Required_Degree": degree_label(req_deg),
            "Degree_Match": "Yes" if degree_ok else "No",
            "Field_Match": "Yes" if field_ok else "No",
            "AI_Score": round(float(prediction), 2),
            "Status": "Shortlisted" if degree_ok and prediction >= 70 else "Not Shortlisted"
        }

    except Exception as e:
        return {
            "Candidate": filename,
            "Skills": "Error",
            "Skill_Percent": 0,
            "Experience": "Error",
            "Degree": "Error",
            "Required_Degree": "Error",
            "Degree_Match": "No",
            "Field_Match": "No",
            "AI_Score": 0,
            "Status": f"Error reading file: {str(e)}"
        }


def analyze_recruiter_files(uploaded_files, job):
    results = []

    for file in uploaded_files:
        filename = file.filename
        data = file.read()

        if filename.lower().endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for f in z.namelist():
                    if f.lower().endswith(".pdf"):
                        pdf_data = z.open(f).read()
                        results.append(analyze_cv(f, pdf_data, job))

        elif filename.lower().endswith(".pdf"):
            results.append(analyze_cv(filename, data, job))

    results = sorted(results, key=lambda x: x["AI_Score"], reverse=True)
    return results
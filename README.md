# AI CV Analyzer & Candidate Ranking System

## Overview

AI CV Analyzer is an intelligent recruitment support system developed using Flask, Machine Learning, and NLP techniques. The system helps applicants analyze their CVs and enables recruiters to rank candidates automatically based on job requirements.

The project extracts CV information from PDF files, compares skills, experience, degree, and field requirements, and generates an AI-based suitability score for candidate shortlisting.

---

# Features

## Applicant Mode
- Upload single CV
- Skill matching analysis
- Experience verification
- Degree and field matching
- AI score prediction
- Shortlist status generation

## Recruiter Mode
- Upload multiple CVs or ZIP files
- Automatic candidate ranking
- AI-based score comparison
- Candidate shortlist generation
- Recruiter dashboard interface

---

# Technologies Used

- Python
- Flask
- Machine Learning
- NLP
- PDF Processing
- HTML
- CSS
- JavaScript
- Scikit-learn
- Joblib
- Pdfplumber

---

# Project Structure

```text
AI-CV-Analyzer/
│
├── app.py
├── analyzer.py
├── cv_model.pkl
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── recruiter_result.html
│
└── static/
    └── style.css
```

---

# How It Works

1. User uploads CV PDF files
2. System extracts CV text
3. Skills, experience, degree, and field are analyzed
4. Machine Learning model predicts AI suitability score
5. Candidate is shortlisted or rejected

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-CV-Analyzer.git
```

## Open Project Folder

```bash
cd AI-CV-Analyzer
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run Project

```bash
python app.py
```

---

# Screenshots

Add project screenshots here after uploading them.

---

# Future Improvements

- Firebase integration
- Deep Learning models
- Real-time recruiter analytics
- Resume improvement suggestions
- Cloud deployment

---

# Developed By

Abubakar Farooq  
BSIT - Bahria University Lahore Campus

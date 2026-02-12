# Candidate Readiness & Skill Gap Explanation System



## Overview

An explainable AI backend that evaluates PDF resumes against predefined role archetypes and generates a recruiter-friendly readiness report. The system combines rule-based extraction, fuzzy matching, and semantic similarity to compute a weighted readiness score, identify capability gaps, and estimate effort to bridge them.

## Features

- PDF resume parsing (PyMuPDF)
- Skill extraction with synonyms map
- Direct, fuzzy (RapidFuzz), and semantic (Sentence-Transformers) matching
- Weighted readiness scoring and gap severity estimation
- Bridgeability effort (weeks per gap)
- Interactive FastAPI web demo with single and bulk evaluation
- Deployable to Render

## Tech Stack

- Python 3.11+ (recommended)
- FastAPI
- sentence-transformers
- RapidFuzz
- PyMuPDF
- scikit-learn
- numpy
- torch
- Jinja2

## How it works

1. Resume PDF → text extraction using PyMuPDF.
2. Extract skills and experience heuristically from the resume text.
3. Load role archetype from `config/roles.json` (core and secondary skills).
4. Match candidate skills to role using direct match, fuzzy matching, and semantic embedding similarity.
5. Compute a weighted readiness score (core skills higher weight), adjust for experience, and identify gaps and their severities.
6. Estimate bridgeability (weeks to learn) per gap and generate a human-readable recruiter report.

## Local setup

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the development server:

```powershell
uvicorn src.main:app --reload
```

Open the demo at: `http://127.0.0.1:8000/`



## File structure

See:

```
candidate-jd-system/
├── config/roles.json
├── data/sample_resume.pdf
├── src/
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html
│   ├── resume_parser.py
│   ├── embedding_engine.py
│   ├── matcher.py
│   ├── hybrid_evaluator.py
│   ├── report_generator.py
│   ├── role_loader.py
│   ├── pipeline.py
│   ├── main.py
│   └── __init__.py
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
```

## Future improvements

- Batch comparison dashboard and downloadable reports
- Skill similarity heatmaps
- Authentication and audit logging for enterprise use

## License

This repository is provided as-is for demonstration and educational purposes.


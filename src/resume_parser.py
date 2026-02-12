from pathlib import Path
from typing import List, Dict
import fitz
import re
from dateutil import parser as dateparser


def extract_text_from_pdf(path: Path) -> str:
    doc = fitz.open(str(path))
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)


def extract_experience_years(text: str) -> float:
    # Simple heuristic: look for patterns like '3 years' or 'Jan 2019 - Feb 2021'
    m = re.search(r"(\d+)\s+years", text, flags=re.I)
    if m:
        try:
            return float(m.group(1))
        except Exception:
            pass

    # Fallback: count distinct year mentions
    years = re.findall(r"(20\d{2}|19\d{2})", text)
    if years:
        unique = sorted(set(int(y) for y in years))
        if len(unique) >= 2:
            return float(unique[-1] - unique[0])
    return 0.0


def extract_skills_from_text(text: str, skill_list: List[str]) -> List[str]:
    found = set()
    lowered = text.lower()
    for skill in skill_list:
        key = skill.lower()
        # word boundary match
        pattern = r"\b" + re.escape(key) + r"\b"
        if re.search(pattern, lowered):
            found.add(skill)
    return sorted(found)


def parse_resume(path: Path, skill_list: List[str]) -> Dict:
    text = extract_text_from_pdf(path)
    years = extract_experience_years(text)
    skills = extract_skills_from_text(text, skill_list)
    return {"text": text, "experience_years": years, "skills": skills}

from typing import List
import re


def parse_jd_text(text: str) -> str:
    return text


def extract_requirements(text: str, skill_list: List[str]) -> List[str]:
    lowered = text.lower()
    found = set()
    for skill in skill_list:
        key = skill.lower()
        pattern = r"\b" + re.escape(key) + r"\b"
        if re.search(pattern, lowered):
            found.add(skill)
    return sorted(found)

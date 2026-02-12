from typing import Dict, List

# A small synonyms map to support capability-based matching
SKILL_SYNONYMS: Dict[str, List[str]] = {
    "python": ["py", "python3"],
    "javascript": ["js", "nodejs"],
    "react": ["reactjs"],
    "sql": ["postgresql", "mysql", "mariadb"],
    "nosql": ["mongodb", "cassandra"],
    "docker": ["containerization"],
    "ci/cd": ["ci", "cd", "jenkins", "github actions"],
    "rest apis": ["rest", "restful"],
    "machine learning": ["ml", "deep learning"],
    "pytorch": ["torch"],
    "kubernetes": ["k8s"]
}


def canonicalize(skill: str) -> str:
    s = skill.strip().lower()
    return s


def expand_skill_list(skills: List[str]) -> List[str]:
    out = set()
    for s in skills:
        cs = canonicalize(s)
        out.add(cs)
        # add synonyms
        for k, vals in SKILL_SYNONYMS.items():
            if cs == k or cs in vals:
                out.add(k)
                for v in vals:
                    out.add(v)
    return sorted(out)

from typing import List, Dict, Tuple
from math import ceil

WEIGHTS = {"high": 1.5, "medium": 1.0, "low": 0.5}


def compute_readiness(required: Dict[str, List[str]], candidate: Dict, matches: Dict) -> Dict:
    # required has core_skills and secondary_skills
    core = required.get("core_skills", [])
    secondary = required.get("secondary_skills", [])

    total_weight = 0.0
    score = 0.0
    gaps = []

    # helper
    def consume(skill: str, importance: str):
        nonlocal total_weight, score
        w = WEIGHTS.get(importance, 1.0)
        total_weight += w
        present = skill in candidate.get("skills", [])
        sem = any(t[0] == skill for t in matches.get("semantic", []))
        fz = any(t[0] == skill for t in matches.get("fuzzy", []))
        direct = skill in matches.get("direct", [])
        if direct or sem or fz:
            # presence score scaled to weight
            score += w
            return True
        else:
            # record gap severity by importance
            sev = 0.7 if importance == "high" else 0.4 if importance == "medium" else 0.2
            gaps.append({"skill": skill, "importance": importance, "severity": sev})
            return False

    for s in core:
        consume(s, "high")
    for s in secondary:
        consume(s, "medium")

    # experience adjustment
    req_years = required.get("experience", {}).get("years", 0)
    cand_years = candidate.get("experience_years", 0)
    exp_factor = 1.0
    if req_years > 0:
        exp_factor = min(1.0, cand_years / req_years)

    raw_pct = (score / total_weight) * 100 if total_weight > 0 else 0.0
    fit_score = raw_pct * exp_factor

    # Bridgeability estimate: simple weeks estimate based on severity
    bridgeability = {}
    for g in gaps:
        weeks = ceil(g["severity"] * 12)  # rough estimator
        bridgeability[g["skill"]] = {"weeks_estimate": weeks, "severity": g["severity"]}

    # readiness level
    if fit_score >= 80:
        readiness = "High Readiness"
    elif fit_score >= 60:
        readiness = "Moderate Readiness"
    elif fit_score >= 40:
        readiness = "Limited Alignment"
    else:
        readiness = "Significant Gaps"

    # risk level
    if fit_score >= 80:
        risk = "low"
    elif fit_score >= 60:
        risk = "medium"
    else:
        risk = "high"

    strengths = [s for s in candidate.get("skills", []) if s in core or s in secondary]

    return {
        "fit_score": round(max(0.0, min(100.0, fit_score)), 1),
        "readiness_level": readiness,
        "risk_level": risk,
        "strengths": strengths,
        "gaps": gaps,
        "bridgeability": bridgeability
    }

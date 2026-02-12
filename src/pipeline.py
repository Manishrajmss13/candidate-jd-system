from pathlib import Path
from typing import Dict, List
from .role_loader import get_role
from .skill_map import expand_skill_list
from .resume_parser import parse_resume
from .jd_parser import extract_requirements
from .embedding_engine import EmbeddingEngine
from .matcher import direct_match, fuzzy_match, semantic_match
from .hybrid_evaluator import compute_readiness
from .report_generator import generate_report


def evaluate_resume(resume_path: Path, role_name: str, jd_text: str | None = None) -> Dict:
    role = get_role(role_name)
    if role is None:
        raise ValueError(f"Unknown role: {role_name}")

    # build skill universe from role
    required_skills = list(set(role.get("core_skills", []) + role.get("secondary_skills", [])))
    # expand
    skill_universe = expand_skill_list(required_skills)

    candidate = parse_resume(resume_path, skill_universe)

    jd_skills = []
    if jd_text:
        jd_skills = extract_requirements(jd_text, skill_universe)

    # embeddings for semantic match
    emb_engine = EmbeddingEngine()
    cand_embs = emb_engine.embed(candidate.get("skills", []))
    req_embs = emb_engine.embed(required_skills)

    matches = {
        "direct": direct_match(candidate.get("skills", []), required_skills),
        "fuzzy": fuzzy_match(candidate.get("skills", []), required_skills),
        "semantic": semantic_match(candidate.get("skills", []), required_skills, cand_embs, req_embs)
    }

    evaluation = compute_readiness(role, candidate, matches)
    report = generate_report(evaluation, role_name)
    # include some internals for transparency
    report["internal_matches"] = matches
    report["candidate_profile"] = {"experience_years": candidate.get("experience_years"), "skills": candidate.get("skills")}
    return report

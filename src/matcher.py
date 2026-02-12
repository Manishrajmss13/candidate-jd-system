from typing import List, Tuple
from rapidfuzz import fuzz
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


SEMANTIC_THRESHOLD = 0.65
FUZZY_THRESHOLD = 85


def direct_match(candidate_skills: List[str], required_skills: List[str]) -> List[str]:
    cset = set(s.lower() for s in candidate_skills)
    out = [s for s in required_skills if s.lower() in cset]
    return out


def fuzzy_match(candidate_skills: List[str], required_skills: List[str]) -> List[Tuple[str, str, int]]:
    matches = []
    for req in required_skills:
        best = (None, 0)
        for cand in candidate_skills:
            score = fuzz.ratio(req.lower(), cand.lower())
            if score > best[1]:
                best = (cand, score)
        if best[1] >= FUZZY_THRESHOLD:
            matches.append((req, best[0], int(best[1])))
    return matches


def semantic_match(candidate_skills: List[str], required_skills: List[str], cand_embs: np.ndarray, req_embs: np.ndarray) -> List[Tuple[str, str, float]]:
    if len(cand_embs) == 0 or len(req_embs) == 0:
        return []
    sims = cosine_similarity(req_embs, cand_embs)
    results = []
    for i, req in enumerate(required_skills):
        j = sims[i].argmax()
        score = float(sims[i][j])
        if score >= SEMANTIC_THRESHOLD:
            results.append((req, candidate_skills[j], score))
    return results

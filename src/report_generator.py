from typing import Dict, List


def generate_report(evaluation: Dict, role_name: str, candidate_name: str = "Candidate") -> Dict:
    explanation_lines: List[str] = []
    explanation_lines.append(f"Role: {role_name}")
    explanation_lines.append(f"Candidate: {candidate_name}")
    explanation_lines.append(f"Fit Score: {evaluation['fit_score']}%")
    explanation_lines.append(f"Readiness: {evaluation['readiness_level']}")
    explanation_lines.append(f"Risk Level: {evaluation['risk_level']}")

    if evaluation.get("strengths"):
        explanation_lines.append("Strength Areas: " + ", ".join(evaluation["strengths"]))

    if evaluation.get("gaps"):
        gap_lines = [f"{g['skill']} (severity {g['severity']})" for g in evaluation["gaps"]]
        explanation_lines.append("Capability Gaps: " + ", ".join(gap_lines))

    explanation_lines.append("Estimated effort to bridge gaps (weeks per skill) available in bridgeability.")

    explanation = "\n".join(explanation_lines)

    return {
        "fit_score": evaluation["fit_score"],
        "readiness_level": evaluation["readiness_level"],
        "risk_level": evaluation["risk_level"],
        "strengths": evaluation.get("strengths", []),
        "gaps": evaluation.get("gaps", []),
        "bridgeability": evaluation.get("bridgeability", {}),
        "explanation": explanation
    }

from pathlib import Path
import sys

# Ensure project root is on sys.path when running this script directly
if __package__ is None:
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root))

from src.pipeline import evaluate_resume
from src.role_loader import load_roles


def run_test():
    root = Path(__file__).resolve().parent.parent
    sample = root / "data" / "sample_resume.pdf"
    roles = load_roles()
    role_name = "Backend Engineer"
    if role_name not in roles:
        print("Role not found in roles.json")
        return

    report = evaluate_resume(sample, role_name)
    print("=== Recruiter Report ===")
    print(report.get("explanation"))
    print("JSON Summary:")
    print({
        "fit_score": report.get("fit_score"),
        "readiness_level": report.get("readiness_level"),
        "risk_level": report.get("risk_level")
    })


if __name__ == "__main__":
    run_test()

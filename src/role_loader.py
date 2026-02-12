from pathlib import Path
import json
from typing import Dict


def load_roles() -> Dict[str, dict]:
    root = Path(__file__).resolve().parent.parent
    roles_path = root / "config" / "roles.json"
    with open(roles_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_role(role_name: str) -> dict | None:
    roles = load_roles()
    return roles.get(role_name)

import json
from pathlib import Path


def load_domain_data(path=None):
    """Load the domain knowledge base and validate its expected top-level fields."""
    if path is None:
        base_dir = Path(__file__).resolve().parent
        candidates = [
            base_dir / "domain_knowledge_base.json",
            base_dir / "domain_knowledge_base.md"
        ]
        for candidate in candidates:
            if candidate.exists():
                path = candidate
                break
        else:
            raise FileNotFoundError(
                "No domain knowledge file found in the project directory."
            )

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    required_fields = {"skills", "misconceptions", "questions"}
    missing_fields = required_fields - set(data.keys())
    if missing_fields:
        raise ValueError(
            f"Domain knowledge file is missing required top-level fields: {sorted(missing_fields)}"
        )

    return data

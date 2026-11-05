import json

from google.genai import types

try:
    from person_c.config import get_gemini_client, get_model_name
    from person_c.domain_loader import load_domain_data
except ImportError:  # pragma: no cover
    from config import get_gemini_client, get_model_name
    from domain_loader import load_domain_data


domain_data = load_domain_data()
_client = None
_model_name = None


def _get_client():
    global _client
    if _client is None:
        _client = get_gemini_client()
    return _client


def _get_model_name():
    global _model_name
    if _model_name is None:
        _model_name = get_model_name()
    return _model_name


def generate_hint(student_code, diagnosis, hint_level, skill="SKL-02"):
    hint_instructions = {
        "L1": "Give only one guiding question. Do not explain the answer.",
        "L2": "Give a conceptual explanation without writing corrected code.",
        "L3": "Give a similar but different worked example. Do not solve the student's exact problem.",
        "L4": "Give a partial solution with meaningful blanks. Never provide the complete solution."
    }

    if hint_level not in hint_instructions:
        raise ValueError("Hint level must be L1, L2, L3, or L4")

    prompt = f"""
    You are a friendly personal Data Structures tutor.

    Student skill: {skill}

    Student's code:
    {student_code}

    Diagnosis:
    {json.dumps(diagnosis)}

    Requested hint level: {hint_level}

    Instructions:
    {hint_instructions[hint_level]}

    Rules:
    1. Focus on the identified misconception.
    2. Use simple beginner-friendly language.
    3. Never reveal the complete solution.
    4. Do not give the answer directly at L1 or L2.
    5. At L3, use a different example.
    6. At L4, leave meaningful blanks in the code.
    7. Keep the hint short and useful.

    Return JSON in this format:

    {{
        "hint_level": "{hint_level}",
        "hint": "Your personalised hint"
    }}
    """

    try:
        response = _get_client().models.generate_content(
            model=_get_model_name(),
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        hint_result = json.loads(response.text)

        if hint_result.get("hint_level") != hint_level:
            raise ValueError("Incorrect hint level returned")

        if not isinstance(hint_result.get("hint"), str):
            raise ValueError("Invalid hint format")

        if not hint_result["hint"].strip():
            raise ValueError("Empty hint returned")

        return hint_result

    except Exception as exc:
        return {
            "hint_level": hint_level,
            "hint": "Hint generation is temporarily unavailable. Please try again.",
            "error": str(exc)
        }


def generate_catalogue_hint(misconception_id, hint_level):
    misconception = next(
        (
            item for item in domain_data["misconceptions"]
            if item["id"] == misconception_id
        ),
        None
    )

    if misconception is None:
        return "Misconception not found."

    if hint_level not in misconception["hints"]:
        return "Hint level not available."

    return misconception["hints"][hint_level]


def get_personalized_hint(student_code, diagnosis, hint_level):
    misconception_id = diagnosis["misconception_id"]
    official_ids = {item["id"] for item in domain_data["misconceptions"]}

    if misconception_id in official_ids:
        hint = generate_catalogue_hint(misconception_id, hint_level)
        return {
            "hint_level": hint_level,
            "hint": hint,
            "hint_source": "person_a_catalogue"
        }

    hint_result = generate_hint(student_code, diagnosis, hint_level)
    hint_result["hint_source"] = "gemini"
    return hint_result

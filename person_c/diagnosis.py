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


def diagnose_error(runner_result, skill="SKL-02"):
    error_type = runner_result.get("error_type")
    traceback = runner_result.get("traceback") or ""

    if error_type == "TIMEOUT":
        misconception_id = "MIS-04"
    elif "NoneType" in traceback:
        misconception_id = "MIS-02"
    elif error_type in ["ASSERTION_ERROR", "RUNTIME_ERROR"]:
        misconception_id = "MC_UNKNOWN"
    else:
        misconception_id = None

    if misconception_id not in [None, "MC_UNKNOWN"]:
        misconception = next(
            item for item in domain_data["misconceptions"]
            if item["id"] == misconception_id
        )

        return {
            "skill": skill,
            "misconception_id": misconception["id"],
            "misconception": misconception["name"],
            "confidence": 0.85,
            "evidence": traceback or "Code execution timed out."
        }

    return {
        "skill": skill,
        "misconception_id": misconception_id,
        "misconception": "Unknown misconception",
        "confidence": 0.40,
        "evidence": traceback or "Incorrect output."
    }


def diagnose_with_gemini(student_code, runner_result, skill="SKL-02"):
    catalogue = []
    for item in domain_data["misconceptions"]:
        catalogue.append({
            "id": item["id"],
            "name": item["name"],
            "root_cause": item["root_cause"],
            "deterministic_trigger": item["deterministic_trigger"]
        })

    prompt = f"""
    You are an expert Python and Data Structures tutor.

    Identify the most likely misconception in the student's code.

    Student skill: {skill}

    Student code:
    {student_code}

    Execution result:
    {json.dumps(runner_result)}

    OFFICIAL MISCONCEPTION CATALOGUE:
    {json.dumps(catalogue, indent=2)}

    Instructions:
1. Analyse the student's code and execution result carefully.
2. Compare the mistake with every official misconception.
3. Select an ID ONLY when the root cause clearly matches.
4. Do not select a misconception just because it sounds similar.
5. MIS-06 is specifically about incorrect position indexing
   during insertion or deletion, NOT skipping nodes during traversal.
6. If no official misconception accurately matches, return MC_UNKNOWN.
7. Never invent an ID.
8. Do not provide the complete corrected solution.

If the student uses current.next.next during normal
linked-list traversal, check whether any official
misconception explicitly covers skipping nodes.
If none does, return MC_UNKNOWN.
    Return JSON with these fields:
    {{
        "skill": "{skill}",
        "misconception_id": "MIS-01",
        "misconception": "Misconception name",
        "confidence": 0.0,
        "evidence": "Evidence from the student's code"
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

        diagnosis = json.loads(response.text)

        allowed_ids = {item["id"] for item in domain_data["misconceptions"]}

        required_keys = [
            "skill",
            "misconception_id",
            "misconception",
            "confidence",
            "evidence"
        ]

        for key in required_keys:
            if key not in diagnosis:
                raise ValueError(f"Missing field: {key}")

        if diagnosis["misconception_id"] not in allowed_ids | {"MC_UNKNOWN"}:
            raise ValueError("Gemini returned an invalid misconception ID")

        confidence = float(diagnosis["confidence"])
        if not 0 <= confidence <= 1:
            raise ValueError("Invalid confidence value")

        diagnosis["confidence"] = confidence

        if diagnosis["misconception_id"] in allowed_ids:
            official_item = next(
                item for item in domain_data["misconceptions"]
                if item["id"] == diagnosis["misconception_id"]
            )
            diagnosis["misconception"] = official_item["name"]

        return diagnosis

    except Exception as exc:
        return {
            "skill": skill,
            "misconception_id": "MC_UNKNOWN",
            "misconception": "Diagnosis unavailable",
            "confidence": 0.0,
            "evidence": str(exc)
        }


def diagnose_student_submission(student_code, runner_result, skill="SKL-02"):
    rule_result = diagnose_error(runner_result, skill)

    if rule_result["misconception_id"] not in [None, "MC_UNKNOWN"]:
        rule_result["diagnosis_source"] = "rule_based"
        return rule_result

    if runner_result.get("passed"):
        rule_result["diagnosis_source"] = "rule_based"
        return rule_result

    gemini_result = diagnose_with_gemini(
        student_code,
        runner_result,
        skill
    )
    gemini_result["diagnosis_source"] = "gemini"
    return gemini_result

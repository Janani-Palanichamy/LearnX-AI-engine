from fastapi.testclient import TestClient

from person_c import api
from person_c import diagnosis as diagnosis_module
from person_c import hint_generator as hint_module


client = TestClient(api.app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "Person C LearnX Python API"
    }


def test_analyze_returns_execution_diagnosis_and_catalogue_hint(monkeypatch):
    runner_result = {
        "passed": False,
        "error_type": "TIMEOUT",
        "output": "",
        "traceback": "Code execution exceeded the time limit."
    }
    monkeypatch.setattr(api, "run_student_code", lambda *args, **kwargs: runner_result)

    response = client.post("/analyze", json={
        "student_code": "while True: pass",
        "test_code": "",
        "skill": "SKL-02",
        "hint_level": "L1",
        "timeout": 3
    })

    assert response.status_code == 200
    result = response.json()
    assert result["runner_result"] == runner_result
    assert result["diagnosis"]["misconception_id"] == "MIS-04"
    assert result["diagnosis"]["diagnosis_source"] == "rule_based"
    assert result["hint"]["hint_source"] == "person_a_catalogue"
    assert result["hint"]["hint_level"] == "L1"
    assert result["hint"]["hint"]


def test_analyze_uses_mocked_gemini_fallbacks(monkeypatch):
    runner_result = {
        "passed": False,
        "error_type": "RUNTIME_ERROR",
        "output": "",
        "traceback": "NameError: name 'missing' is not defined"
    }
    monkeypatch.setattr(api, "run_student_code", lambda *args, **kwargs: runner_result)
    monkeypatch.setattr(
        diagnosis_module,
        "diagnose_with_gemini",
        lambda student_code, result, skill: {
            "skill": skill,
            "misconception_id": "MC_UNKNOWN",
            "misconception": "Unknown misconception",
            "confidence": 0.4,
            "evidence": "No official match."
        }
    )
    monkeypatch.setattr(
        hint_module,
        "generate_hint",
        lambda student_code, diagnosis, hint_level: {
            "hint_level": hint_level,
            "hint": "Check the variable name in your code."
        }
    )

    response = client.post("/analyze", json={
        "student_code": "print(missing)",
        "test_code": "",
        "hint_level": "L2"
    })

    assert response.status_code == 200
    result = response.json()
    assert result["diagnosis"]["diagnosis_source"] == "gemini"
    assert result["diagnosis"]["misconception_id"] == "MC_UNKNOWN"
    assert result["hint"] == {
        "hint_level": "L2",
        "hint": "Check the variable name in your code.",
        "hint_source": "gemini"
    }


def test_diagnose_returns_execution_and_diagnosis_without_hint(monkeypatch):
    runner_result = {
        "passed": True,
        "error_type": None,
        "output": "ok",
        "traceback": None
    }
    monkeypatch.setattr(api, "run_student_code", lambda *args, **kwargs: runner_result)

    response = client.post("/diagnose", json={
        "student_code": "print('ok')",
        "test_code": ""
    })

    assert response.status_code == 200
    result = response.json()
    assert result["runner_result"] == runner_result
    assert result["diagnosis"]["misconception_id"] is None
    assert "hint" not in result


def test_invalid_hint_level_returns_422():
    response = client.post("/analyze", json={
        "student_code": "print('ok')",
        "test_code": "",
        "hint_level": "L5"
    })

    assert response.status_code == 422


def test_missing_student_code_returns_422():
    response = client.post("/analyze", json={"test_code": ""})

    assert response.status_code == 422

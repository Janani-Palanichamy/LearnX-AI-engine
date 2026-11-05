from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from person_c.code_runner import run_student_code
from person_c.diagnosis import diagnose_student_submission
from person_c.hint_generator import get_personalized_hint


class AnalyzeRequest(BaseModel):
    student_code: str = Field(min_length=1)
    test_code: str
    skill: str = "SKL-02"
    hint_level: Literal["L1", "L2", "L3", "L4"] = "L1"
    timeout: float = Field(default=3, gt=0, le=30)


app = FastAPI(title="Person C LearnX Python API")


def _run_and_diagnose(request: AnalyzeRequest):
    runner_result = run_student_code(
        request.student_code,
        request.test_code,
        timeout=request.timeout
    )
    diagnosis = diagnose_student_submission(
        request.student_code,
        runner_result,
        request.skill
    )
    return runner_result, _sanitize_diagnosis(diagnosis)


def _sanitize_diagnosis(diagnosis):
    result = dict(diagnosis)
    if result.get("misconception") == "Diagnosis unavailable":
        result["evidence"] = "Gemini diagnosis is temporarily unavailable."
    return result


def _sanitize_hint(hint):
    result = dict(hint)
    if "error" in result:
        result["error"] = "Hint generation is temporarily unavailable."
    return result


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Person C LearnX Python API"
    }


@app.post("/analyze")
def analyze_submission(request: AnalyzeRequest):
    runner_result, diagnosis = _run_and_diagnose(request)
    hint = get_personalized_hint(
        request.student_code,
        diagnosis,
        request.hint_level
    )
    return {
        "runner_result": runner_result,
        "diagnosis": diagnosis,
        "hint": _sanitize_hint(hint)
    }


@app.post("/diagnose")
def diagnose_submission(request: AnalyzeRequest):
    runner_result, diagnosis = _run_and_diagnose(request)
    return {
        "runner_result": runner_result,
        "diagnosis": diagnosis
    }

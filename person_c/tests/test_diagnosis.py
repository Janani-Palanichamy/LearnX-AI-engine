from person_c.diagnosis import diagnose_error, diagnose_student_submission


def test_diagnose_error_timeout():
    result = diagnose_error({
        "passed": False,
        "error_type": "TIMEOUT",
        "output": "",
        "traceback": "Code execution exceeded the time limit."
    })
    assert result["misconception_id"] == "MIS-04"


def test_diagnose_error_runtime_error_known_misconception():
    result = diagnose_error({
        "passed": False,
        "error_type": "RUNTIME_ERROR",
        "output": "",
        "traceback": "AttributeError: 'NoneType' object has no attribute 'next'"
    })
    assert result["misconception_id"] == "MIS-02"


def test_diagnose_student_submission_uses_rule_based_unknown_result():
    result = diagnose_student_submission(
        "while True:\n    pass\n",
        {"passed": False, "error_type": "TIMEOUT", "output": "", "traceback": "Code execution exceeded the time limit."}
    )
    assert result["diagnosis_source"] == "rule_based"
    assert result["misconception_id"] == "MIS-04"

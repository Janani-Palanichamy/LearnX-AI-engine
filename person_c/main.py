import json

try:
    from person_c.code_runner import run_student_code
    from person_c.diagnosis import diagnose_student_submission
    from person_c.hint_generator import get_personalized_hint
except ImportError:  # pragma: no cover
    from code_runner import run_student_code
    from diagnosis import diagnose_student_submission
    from hint_generator import get_personalized_hint


def main():
    student_code = """
while True:
    pass
"""

    test_code = """
print("Testing")
"""

    runner_result = run_student_code(student_code, test_code, timeout=1)
    diagnosis = diagnose_student_submission(student_code, runner_result)
    hint = get_personalized_hint(student_code, diagnosis, "L1")

    print(json.dumps({
        "runner_result": runner_result,
        "diagnosis": diagnosis,
        "hint": hint
    }, indent=4))


if __name__ == "__main__":
    main()

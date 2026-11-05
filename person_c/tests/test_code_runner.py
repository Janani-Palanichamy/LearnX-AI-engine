from person_c.code_runner import run_student_code


def test_run_student_code_success():
    student_code = """
def add(a, b):
    return a + b
"""
    test_code = """
assert add(5, 3) == 8
assert add(10, 20) == 30
print('All tests passed!')
"""

    result = run_student_code(student_code, test_code)
    assert result["passed"] is True
    assert result["error_type"] is None
    assert result["traceback"] is None


def test_run_student_code_timeout():
    student_code = """
while True:
    pass
"""
    test_code = """
print('Testing')
"""

    result = run_student_code(student_code, test_code, timeout=0.1)
    assert result["passed"] is False
    assert result["error_type"] == "TIMEOUT"

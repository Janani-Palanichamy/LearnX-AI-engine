import os
import subprocess
import sys
import tempfile


def run_student_code(student_code, test_code, timeout=3):
    """Execute a student's code alongside a test script and classify the result."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False,
        encoding="utf-8"
    ) as file:
        file.write(student_code)
        file.write("\n\n")
        file.write(test_code)
        file_path = file.name

    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            return {
                "passed": True,
                "error_type": None,
                "output": result.stdout,
                "traceback": None
            }

        error_line = result.stderr.strip().splitlines()
        return {
            "passed": False,
            "error_type": (
                "ASSERTION_ERROR"
                if "AssertionError" in result.stderr
                else "RUNTIME_ERROR"
            ),
            "output": result.stdout,
            "traceback": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "error_type": "TIMEOUT",
            "output": "",
            "traceback": "Code execution exceeded the time limit."
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

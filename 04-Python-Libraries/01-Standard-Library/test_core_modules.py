"""
# ==============================================================================
# LABORATORY: TESTING CORE STANDARD LIBRARIES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When writing production software, you rely heavily on the Python Standard Library
# (`os`, `sys`, `json`, `pathlib`, `collections`, `itertools`, `datetime`). 
# 
# How do you test code that interacts with the file system, network, or time?
# You cannot rely on physical files (what if the file doesn't exist on the CI/CD 
# server?). You cannot rely on current time (tests will fail tomorrow).
#
# The Solution: Advanced Pytest & Mocking!
# This laboratory demonstrates how to write professional test suites using:
# - `pytest.fixture`: For setting up temporary test environments.
# - `tmp_path`: Pytest's built-in fixture for temporary directories.
# - `unittest.mock.patch`: To intercept and fake standard library calls.
# - `pytest.mark.parametrize`: To test 50 different inputs without writing 50 tests.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master File System testing without touching the real Hard Drive.
# - Master mocking the `datetime` module (Time Travel).
# - Test `collections` and `itertools` robustly.
#
# ==============================================================================
"""

import json
import pathlib
import datetime
from collections import Counter, defaultdict
import pytest
from unittest.mock import patch, MagicMock

# ==============================================================================
# 3. MOCKING THE FILE SYSTEM (PATHLIB & JSON)
# ==============================================================================
def process_user_data(filepath: pathlib.Path) -> dict:
    """A sample function that reads a JSON file and processes it."""
    if not filepath.exists():
        raise FileNotFoundError(f"Missing configuration: {filepath}")
        
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Process data
    data["processed_timestamp"] = datetime.datetime.now().isoformat()
    return data


def test_process_user_data_success(tmp_path):
    """
    Tests file reading using Pytest's brilliant `tmp_path` fixture.
    `tmp_path` creates a temporary directory that is automatically deleted 
    after the test finishes! We NEVER touch the real file system!
    """
    # 1. Setup the fake environment
    fake_dir = tmp_path / "config"
    fake_dir.mkdir()
    fake_file = fake_dir / "user.json"
    
    # 2. Write test data
    test_json = {"user_id": 101, "name": "Ada Lovelace"}
    fake_file.write_text(json.dumps(test_json), encoding="utf-8")
    
    # 3. Execute the function under test
    # We freeze time using `unittest.mock.patch` to guarantee deterministic output!
    mock_time = datetime.datetime(2050, 1, 1, 12, 0, 0)
    
    with patch("datetime.datetime") as mock_dt:
        mock_dt.now.return_value = mock_time
        result = process_user_data(fake_file)
        
    # 4. Assertions
    assert result["user_id"] == 101
    assert result["processed_timestamp"] == "2050-01-01T12:00:00"


def test_process_user_data_missing_file(tmp_path):
    """Tests the error handling of the function."""
    missing_file = tmp_path / "does_not_exist.json"
    
    with pytest.raises(FileNotFoundError) as exc_info:
        process_user_data(missing_file)
        
    assert "Missing configuration" in str(exc_info.value)


# ==============================================================================
# 4. PARAMETRIZED TESTING (COLLECTIONS)
# ==============================================================================
def analyze_text(text: str) -> dict:
    """Uses the `collections` module to analyze a string."""
    chars = Counter(text.lower().replace(" ", ""))
    return dict(chars)


@pytest.mark.parametrize(
    "input_text, expected_counts",
    [
        ("Hello", {"h": 1, "e": 1, "l": 2, "o": 1}),
        ("A a B b", {"a": 2, "b": 2}),
        ("", {}), # Edge case: Empty string
        ("   ", {}), # Edge case: Only whitespace
    ]
)
def test_analyze_text_parametrized(input_text, expected_counts):
    """
    Parametrized tests allow us to run the exact same test logic with multiple 
    different inputs! Pytest will treat this as 4 entirely separate tests.
    """
    result = analyze_text(input_text)
    assert result == expected_counts


# ==============================================================================
# 5. MOCKING STANDARD OUTPUT (SYS.STDOUT)
# ==============================================================================
def print_warning(message: str):
    import sys
    print(f"[WARNING] {message}", file=sys.stderr)


def test_print_warning(capsys):
    """
    Testing print statements is notoriously difficult.
    Pytest provides the `capsys` fixture, which secretly captures everything 
    sent to stdout and stderr!
    """
    print_warning("Database connection lost!")
    
    # Read the captured output
    captured = capsys.readouterr()
    
    # stdout should be empty
    assert captured.out == ""
    # stderr should contain our warning
    assert "[WARNING] Database connection lost!\n" in captured.err


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `tmp_path` superior to `os.makedirs("test_temp")`?
   Answer: State contamination! If your test suite creates physical files in the working directory and crashes halfway through, the files are left behind. The next time you run the tests, they might read the leftover files and pass/fail incorrectly! Pytest's `tmp_path` creates a unique directory in the OS temp folder for EVERY SINGLE TEST, and forcefully deletes it when the test ends. It guarantees a perfectly pristine, isolated environment.

2. Why must we mock `datetime.now()`?
   Answer: Tests must be Deterministic (100% reproducible). If a test asserts that a timestamp string matches exactly, and you run the test tomorrow, the output of `datetime.now()` will have changed, causing the test to fail. By using `unittest.mock.patch` to intercept the call to the standard library, we force the Python interpreter to return a fake, frozen timestamp (e.g., Year 2050). The test becomes mathematically deterministic!

3. How does `@pytest.mark.parametrize` reduce technical debt?
   Answer: Without parametrization, you would have to write `test_analyze_text_hello()`, `test_analyze_text_empty()`, `test_analyze_text_whitespace()`, duplicating the exact same assertion logic 10 times. Parametrization separates the DATA from the LOGIC. You write the logic once, and feed it a massive array of Edge Cases. If you change the function signature later, you only have to update ONE test function, instead of updating 50 duplicated functions.
"""

if __name__ == "__main__":
    print("This is a Pytest file! To execute these tests, run:")
    print("pytest -v test_core_modules.py")
    print("\n[SUCCESS] Laboratory: Testing Core Modules Completed.")

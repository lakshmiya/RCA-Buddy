from app.parsing import extract_error_signature


def test_extracts_step_exception_and_traceback():
    result = extract_error_signature(
        "step: tests\nTraceback (most recent call last):\nImportError: package missing"
    )
    assert result.failing_step == "tests"
    assert result.exception_type == "ImportError"
    assert "Traceback" in result.stack_trace


def test_empty_log_is_safe():
    result = extract_error_signature("")
    assert result.exception_type == "unknown error"
    assert result.relevant_lines == []

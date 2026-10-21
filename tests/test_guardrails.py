
import pytest

from app.guardrails.input_checks import validate_input
from app.guardrails.injection_checks import check_prompt_injection
from app.guardrails.content_safety import check_content_safety
from app.guardrails.output_validation import validate_output


def test_valid_input():
    result = validate_input("Show customer analytics")

    assert result == "Show customer analytics"


def test_empty_input_is_rejected():
    with pytest.raises(ValueError):
        validate_input("   ")


def test_input_length_limit():
    with pytest.raises(ValueError):
        validate_input("a" * 2001)


def test_normal_query_passes_injection_check():
    result = check_prompt_injection("Find active customers")

    assert result is not None


def test_normal_query_passes_content_safety():
    result = check_content_safety("Show subscription statistics")

    assert result is not None


def test_valid_output():
    result = validate_output("There are 100 active customers.")

    assert result is not None

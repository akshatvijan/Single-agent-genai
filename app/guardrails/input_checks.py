
def validate_input(text: str, max_length: int = 2000) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    text = text.strip()

    if not text:
        raise ValueError("Input cannot be empty.")

    if len(text) > max_length:
        raise ValueError(
            f"Input cannot exceed {max_length} characters."
        )

    return text

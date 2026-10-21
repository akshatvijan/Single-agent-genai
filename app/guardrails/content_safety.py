
def check_content_safety(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    if not text.strip():
        raise ValueError("Input cannot be empty.")

    return text
 

def validate_output(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("The agent returned an invalid response.")

    text = text.strip()

    if not text:
        raise ValueError("The agent returned an empty response.")

    return text


import os

from dotenv import load_dotenv

load_dotenv()


def setup_langfuse():
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    base_url = os.getenv("LANGFUSE_BASE_URL")

    if not public_key or not secret_key or not base_url:
        print("Langfuse credentials missing. Tracing disabled.")
        return False

    try:
        from langfuse import get_client
        from pydantic_ai import Agent

        Agent.instrument_all()

        client = get_client()

        if client.auth_check():
            print("Langfuse connected successfully.")
            return True

        print("Langfuse authentication failed.")
        return False

    except Exception as exc:
        print(f"Langfuse setup failed: {exc}")
        return False

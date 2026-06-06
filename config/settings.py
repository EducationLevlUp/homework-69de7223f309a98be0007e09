"""Configuration module for the deep research agent."""

from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_llm_model() -> str:
    """Return the LLM model identifier in provider:model format."""
    import os

    return os.getenv("LLM_MODEL", "openai:gpt-4o")


def get_openai_api_key() -> str | None:
    """Return the OpenAI API key if set, else None."""
    import os

    return os.getenv("OPENAI_API_KEY")


def get_export_dir() -> Path:
    """Return the target directory for exporting virtual files."""
    import os

    default = Path("./exported_files")
    return Path(os.getenv("EXPORT_DIR", str(default)))


def get_thread_id() -> str:
    """Return the thread ID for the agent session, generating one if not set."""
    import os
    import uuid

    thread_id = os.getenv("THREAD_ID")
    if thread_id:
        return thread_id
    return str(uuid.uuid4())

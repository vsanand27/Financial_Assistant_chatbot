"""Central configuration.

The only module that reads the environment / .env file. Everything else imports
its settings from here rather than calling os.getenv directly.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --- Model ------------------------------------------------------------------
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))

# --- Page -------------------------------------------------------------------
PAGE_TITLE = "Financial Assistant"
PAGE_ICON = "💰"
DISCLAIMER = "⚠️ Educational use only. Not licensed financial advice."


def get_api_key() -> str | None:
    """OpenAI API key from the environment, or None if it is not set."""
    return os.getenv("OPENAI_API_KEY")

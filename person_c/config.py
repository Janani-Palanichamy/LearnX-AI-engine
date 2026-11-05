import os

from google import genai


try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv():
        return False


def load_environment():
    load_dotenv()


def get_gemini_client():
    load_environment()
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")
    return genai.Client(api_key=api_key)


def get_model_name():
    load_environment()
    return os.getenv("GEMINI_MODEL_NAME", "gemini-3.6-flash")

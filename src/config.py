import os
from dotenv import load_dotenv

def load_config():
    """
    Loads configuration from environment variables using dotenv.

    Returns:
        dict: A dictionary containing all relevant config values.
    """
    load_dotenv()

    config = {
        "llm_backend": os.getenv("LLM_BACKEND", "openai"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "llama_model_path": os.getenv("LLAMA_MODEL_PATH"),
        "github_token": os.getenv("GITHUB_TOKEN"),
    }

    # Optional: validate required values
    if config["llm_backend"] == "openai" and not config["openai_api_key"]:
        raise ValueError("OPENAI_API_KEY is required when LLM_BACKEND is set to 'openai'")

    if config["llm_backend"] == "llama" and not config["llama_model_path"]:
        raise ValueError("LLAMA_MODEL_PATH is required when LLM_BACKEND is set to 'llama'")

    if not config["github_token"]:
        raise ValueError("GITHUB_TOKEN is required for GitHub API access")

    return config

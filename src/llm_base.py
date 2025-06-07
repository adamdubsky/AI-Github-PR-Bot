from openai_backend import run_openai_prompt
from llama_backend import run_llama_prompt

def get_llm_response(prompt: str, config: dict) -> str:
    """
    Delegates the prompt to the configured LLM backend.

    Args:
        prompt (str): Full prompt (template + injected diff)
        config (dict): Loaded environment config

    Returns:
        str: LLM-generated response
    """
    backend = config.get("llm_backend")

    if backend == "openai":
        return run_openai_prompt(prompt, config)
    elif backend == "llama":
        return run_llama_prompt(prompt, config)
    else:
        raise ValueError(f"Unsupported LLM_BACKEND: {backend}")

from llama_cpp import Llama
import os

_model = None  # Lazy load

def run_llama_prompt(prompt: str, config: dict) -> str:
    """
    Loads and runs a local LLaMA model to get a completion for the prompt.

    Args:
        prompt (str): The full input prompt
        config (dict): Loaded environment config

    Returns:
        str: The LLM-generated response
    """
    global _model

    model_path = config.get("llama_model_path")
    if not model_path or not os.path.exists(model_path):
        return "Error: LLaMA model path is missing or invalid."

    if _model is None:
        _model = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=8,    # Tune based on CPU
            verbose=False
        )

    try:
        response = _model(
            prompt,
            temperature=0.2,
            max_tokens=1024,
            stop=["###"]  # Helps trim output if needed
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error running LLaMA model: {e}"

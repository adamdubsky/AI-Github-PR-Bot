import openai

def run_openai_prompt(prompt: str, config: dict) -> str:
    """
    Sends the prompt to OpenAI GPT-4 and returns the response.

    Args:
        prompt (str): The prompt string to send
        config (dict): Loaded config with OpenAI credentials

    Returns:
        str: Response content from the model
    """
    openai.api_key = config["openai_api_key"]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior software engineer doing code review."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error calling OpenAI API: {e}"

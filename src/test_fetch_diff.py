from config import load_config
from github_api import fetch_pr_diff
from llm_base import get_llm_response

if __name__ == "__main__":
    config = load_config()
    repo = "your-username/your-repo"   # Change this
    pr_number = 1                      # And this

    diff = fetch_pr_diff(repo, pr_number, config)

    with open("prompts/review_prompt.txt", "r") as f:
        base_prompt = f.read()

    full_prompt = base_prompt + "\n\n" + diff
    response = get_llm_response(full_prompt, config)

    print("--- REVIEW START ---")
    print(response)
    print("--- REVIEW END ---")

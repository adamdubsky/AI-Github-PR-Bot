from config import load_config
from github_api import fetch_pr_diff
from llm_base import get_llm_response

import sys
import os

def main(pr_number: int, repo_full_name: str):
    """
    End-to-end driver for reviewing a GitHub PR using AI.
    """
    print(f"Starting review for PR #{pr_number} in repo: {repo_full_name}")
    
    config = load_config()

    try:
        diff = fetch_pr_diff(repo_full_name, pr_number, config)
    except Exception as e:
        print(f"Failed to fetch PR diff: {e}")
        return

    try:
        with open("prompts/review_prompt.txt", "r") as f:
            base_prompt = f.read()
    except FileNotFoundError:
        print("Could not find 'prompts/review_prompt.txt'")
        return

    full_prompt = base_prompt + "\n\n" + diff

    print("🧠 Sending to LLM backend:", config["llm_backend"])
    response = get_llm_response(full_prompt, config)

    print("\n--- AI REVIEW START ---\n")
    print(response)
    print("\n--- AI REVIEW END ---\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/main.py <PR_NUMBER> <REPO_FULL_NAME>")
        print("Example: python src/main.py 42 octocat/Hello-World")
    else:
        pr_number = int(sys.argv[1])
        repo_full_name = sys.argv[2]
        main(pr_number, repo_full_name)

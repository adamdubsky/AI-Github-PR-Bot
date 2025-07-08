import time
import logging
from urllib.parse import urlparse

from config import load_config
from github_api import fetch_pr_diff, post_review_comment, check_existing_comment, list_open_pull_requests
from llm_base import get_llm_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("ai_pr_bot.log"),
        logging.StreamHandler()
    ]
)

def parse_repo_url(repo_url: str) -> str:
    """Converts full GitHub URL to owner/repo format."""
    if "github.com" in repo_url:
        parts = urlparse(repo_url)
        path_parts = parts.path.strip("/").split("/")
        if len(path_parts) == 2:
            return f"{path_parts[0]}/{path_parts[1]}"
    return repo_url  # fallback if already formatted

def review_pr(pr_number: int, repo_full_name: str, config: dict):
    logging.info(f"Reviewing PR #{pr_number} in {repo_full_name}")

    try:
        diff = fetch_pr_diff(repo_full_name, pr_number, config)
        logging.info(f"Fetched diff for PR #{pr_number}")
    except Exception as e:
        logging.error(f"Failed to fetch PR diff for #{pr_number}: {e}")
        return

    try:
        with open("prompts/review_prompt.txt", "r") as f:
            base_prompt = f.read()
        logging.info("Loaded review prompt")
    except FileNotFoundError:
        logging.error("Missing file: prompts/review_prompt.txt")
        return

    full_prompt = base_prompt + "\n\n" + diff
    logging.info("Sending prompt to LLM")

    try:
        response = get_llm_response(full_prompt, config)
    except Exception as e:
        logging.error(f"LLM backend failed: {e}")
        return

    if not response or len(response.strip()) == 0:
        logging.warning(f"Empty response from LLM for PR #{pr_number}")
        return

    logging.info("LLM responded successfully")

    # Only post if no comment already exists
    if check_existing_comment(repo_full_name, pr_number, config):
        logging.info(f"AI comment already exists on PR #{pr_number} — skipping.")
        return

    try:
        post_review_comment(repo_full_name, pr_number, response, config)
        logging.info(f"Posted comment on PR #{pr_number}")
    except Exception as e:
        logging.error(f"Failed to post review comment: {e}")

def main():
    config = load_config()
    raw_repo_url = config["repo"]
    repo_full_name = parse_repo_url(raw_repo_url)

    logging.info(f"Monitoring repository: {repo_full_name}")

    while True:
        try:
            prs = list_open_pull_requests(repo_full_name, config)
            logging.info(f"Checked {len(prs)} open PR(s)")
            for pr in prs:
                pr_number = pr["number"]
                pr_title = pr["title"]

                if check_existing_comment(repo_full_name, pr_number, config):
                    logging.info(f"Skipping PR #{pr_number} — already reviewed.")
                    continue

                logging.info(f"Reviewing PR #{pr_number} — '{pr_title}'")
                review_pr(pr_number, repo_full_name, config)

        except Exception as e:
            logging.exception(f"Unexpected error during polling: {e}")
        
        time.sleep(180)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted by user — shutting down.")

import requests
import hashlib



def _generate_comment_tag(content: str) -> str:
    """
    Generates a fingerprint tag based on the content.
    This helps detect if we've already posted this review.

    Returns:
        str: Unique tag string embedded in the comment
    """
    hash_digest = hashlib.sha256(content.encode()).hexdigest()[:8]
    return f"<!-- ai-review-{hash_digest} -->"

def check_existing_comment(repo: str, pr_number: int, review_body: str, config: dict) -> bool:
    """
    Checks if a comment with this fingerprint has already been posted to the PR.

    Returns:
        bool: True if already exists, False otherwise
    """
    headers = {
        "Authorization": f"Bearer {config['github_token']}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch PR comments: {resp.status_code} - {resp.text}")

    tag = _generate_comment_tag(review_body)
    comments = resp.json()

    for comment in comments:
        if tag in comment.get("body", ""):
            return True

    return False

def fetch_pr_diff(repo_full_name: str, pr_number: int, config: dict) -> str:
    """
    Fetches the diff for a specific pull request using GitHub REST API.
    
    Args:
        repo_full_name (str): e.g., "username/repo"
        pr_number (int): The PR number
        config (dict): Loaded config containing GitHub token

    Returns:
        str: The unified diff string for the PR (e.g., what you'd send to the LLM)
    """
    headers = {
        "Authorization": f"Bearer {config['github_token']}",
        "Accept": "application/vnd.github.v3.diff"
    }

    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch PR diff: {response.status_code} - {response.text}")

    return response.text

import requests

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

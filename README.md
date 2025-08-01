# AI GitHub Pull Request Reviewer Bot

A production-ready AI-powered tool for automated code review. This bot integrates with GitHub pull requests to provide intelligent, structured feedback using either OpenAI GPT-4 or local LLaMA models.

---

## Overview

The AI PR Reviewer Bot automatically reviews pull requests by:
- Summarizing the proposed code changes
- Identifying potential bugs and edge cases
- Recommending improvements or refactoring opportunities
- Highlighting best practice violations

The review is posted as a well-formatted Markdown comment directly on the pull request. This streamlines the review process, reduces time-to-merge, and improves code quality across the organization.

---

## Example PR Report
https://github.com/adamdubsky/AI-Github-PR-Bot/pull/3
<img width="937" alt="image" src="https://github.com/user-attachments/assets/0f10d2c7-d9b9-4d44-bb2b-f0fda7b9abff" />


---

## Features

- Automated PR review on open/update events
- Markdown-formatted summaries and suggestions
- Supports OpenAI GPT-4 and local `.gguf` models via `llama-cpp-python`
- Smart deduplication to prevent repeat comments
- Configurable, modular, and testable architecture
- CLI support and GitHub Actions integration

---

## Requirements

- Python 3.10+
- OpenAI API Key **or** local `.gguf` model file
- GitHub Personal Access Token (with `repo` and `pull_request` permissions)

---

## Generating a GitHub Personal Access Token

1. Sign in to [github.com](https://github.com) and open **Settings**.
2. Navigate to **Developer settings → Personal access tokens**.
3. Choose **Generate new token** (classic or fine-grained).
4. Set an expiration, give it a descriptive name, and enable the **repo** scope.
5. Click **Generate token** and copy the value.
6. Store the token in your `.env` file under `GITHUB_TOKEN` and keep it secret.

---

## Configuration

Create a `.env` file in the project root based on the `.env.example` template:

```env
LLM_BACKEND=openai                     # or "llama"
OPENAI_API_KEY=sk-...                 # Only if using OpenAI
LLAMA_MODEL_PATH=./models/llama-2-7b.Q4_K_M.gguf  # Only if using llama
GITHUB_TOKEN=ghp_your_token_here      # GitHub token for API access
REPO_URL=https://github.com/yourusername/yourrepo
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/ai-pr-reviewer-bot
cd ai-pr-reviewer-bot

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Bot

```bash
python src/main.py
```
The bot will automatically:
- Monitor the configured GitHub repository (from the .env file)
- Check for open pull requests every 3 minutes
- Detect whether an AI-generated comment already exists
- Generate a new review and post it if none is found



---

## License

MIT License. See `LICENSE` for details.

---

## Designed For

- Internal engineering teams at scale
- AI developer tooling and workflows
- Privacy-sensitive orgs (via local model support)
- OSS and enterprise integrations

---

For questions, support, or contributing, please contact `adamdubsky@gmail.com`.

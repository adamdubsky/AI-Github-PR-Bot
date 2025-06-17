# 🧠 AI GitHub Pull Request Reviewer Bot

A production-ready AI-powered tool for automated code review. This bot integrates with GitHub pull requests to provide intelligent, structured feedback using either OpenAI GPT-4 or local LLaMA models.

---

## 📌 Overview

The AI PR Reviewer Bot automatically reviews pull requests by:
- Summarizing the proposed code changes
- Identifying potential bugs and edge cases
- Recommending improvements or refactoring opportunities
- Highlighting best practice violations

The review is posted as a well-formatted Markdown comment directly on the pull request. This streamlines the review process, reduces time-to-merge, and improves code quality across the organization.

---

## 🚀 Features

- ✅ Automated PR review on open/update events
- ✅ Markdown-formatted summaries and suggestions
- ✅ Supports OpenAI GPT-4 and local `.gguf` models via `llama-cpp-python`
- ✅ Smart deduplication to prevent repeat comments
- ✅ Configurable, modular, and testable architecture
- ✅ CLI support and GitHub Actions integration

---

## 🔐 Requirements

- Python 3.10+
- OpenAI API Key **or** local `.gguf` model file
- GitHub Personal Access Token (with `repo` and `pull_request` permissions)

---

## ⚙️ Configuration

Create a `.env` file in the project root based on the `.env.example` template:

```env
LLM_BACKEND=openai                     # or "llama"
OPENAI_API_KEY=sk-...                 # Only if using OpenAI
LLAMA_MODEL_PATH=./models/model.gguf  # Only if using llama
GITHUB_TOKEN=ghp_...                  # GitHub token for API access
GITHUB_WEBHOOK_SECRET=placeholder     # Reserved for future webhook support
```

---

## 🛠️ Installation

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

## 💻 Running the Bot (Manual Mode)

```bash
python src/main.py <PR_NUMBER> <OWNER/REPO>
```

**Example:**
```bash
python src/main.py 17 octocat/Hello-World
```

This fetches the PR diff, generates a review with the selected LLM, and posts a single structured comment on the PR (if no duplicate exists).

---

## ⚙️ GitHub Action Integration (Optional)

To automate reviews on PR creation or updates, add the following workflow:

```yaml
# .github/workflows/pr-review.yml
name: AI PR Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run PR Reviewer
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        LLM_BACKEND: openai
        GITHUB_WEBHOOK_SECRET: placeholder
      run: |
        python src/main.py ${{ github.event.number }} ${{ github.repository }}
```

Set your secrets under **Repository → Settings → Secrets → Actions**.

---

## 🧠 LLM Prompt Format

The bot uses a consistent, interpretable format:

````markdown
### 📜 Summary
...

### ⚠️ Issues Detected
- (file:line): ...

### ✅ Suggestions for Improvement
- (file:line): ...

### 🧠 Best Practices Check
...
````

---

## 📄 License

MIT License. See `LICENSE` for details.

---

## 🧠 Designed For

- Internal engineering teams at scale
- AI developer tooling and workflows
- Privacy-sensitive orgs (via local model support)
- OSS and enterprise integrations

---

For questions, support, or contributing, please contact `maintainers@yourcompany.com`.

# Day 3 — Python Project Setup and Gemini Configuration

## What We Are Learning

An AI project needs more than Python code. It also needs a consistent environment, managed dependencies, configuration for external services, and a safe way to handle secrets. In this lesson, we set up those foundations so future agent experiments can run reliably and be shared without exposing credentials.

## Learning Objectives

By the end of this lesson, we should be able to:

- Explain why a Python project uses a virtual environment.
- Add and synchronize dependencies with `uv`.
- Store an API key outside the source code.
- Explain the purpose of `.env`, `.env.example`, and `.gitignore`.
- Verify that Python can load the Gemini API key without printing it.
- Run a basic Gemini API call from the project.

## 1. Project Structure

Our project separates runnable Python code from lesson material:

```text
AgenticAI-From-Scratch/
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
├── src/
│   └── agentic_ai_learning/
│       ├── __init__.py
│       └── main.py
└── lessons/
    └── phase-01-foundations/
        └── day-03-project-setup/
            └── README.md
```

The `src/agentic_ai_learning/` folder contains Python code. The `lessons/` folder contains learning notes. Keeping these separate makes it easier to find the code we run and the lesson that explains it.

## 2. Python and Virtual Environments

Python runs our application code. A virtual environment keeps this project's installed packages separate from packages used by other Python projects on the same computer. This helps reduce dependency conflicts and makes the project easier to recreate.

We use `uv` to manage the project environment and dependencies. Running commands through `uv run` makes them use the project's environment.

## 3. Dependencies and `uv`

A dependency is a package our code needs. This project uses:

- `google-genai` to call Gemini.
- `python-dotenv` to load local configuration from a `.env` file.

Useful commands:

| Command | Purpose |
|---|---|
| `uv init` | Creates the initial Python project files. |
| `uv add PACKAGE` | Adds a package as a project dependency. |
| `uv sync` | Synchronizes the environment with the dependencies recorded for the project. |
| `uv run COMMAND` | Runs a command using the project environment. |

`pyproject.toml` records project configuration and dependencies. `uv.lock` records resolved package versions so the environment can be recreated more consistently.

## 4. API Keys and Environment Variables

An API key is a credential that lets an application authenticate with an API provider. Treat it like a password: someone who obtains it may be able to use the associated service or quota.

We store the key locally in a `.env` file at the project root:

```text
GEMINI_API_KEY=your_actual_key_goes_here
```

The `.env` file must not be uploaded to GitHub.

The `.gitignore` file tells Git which files to leave out of version control. It should include:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
```

The `.env.example` file is a safe template that documents the required variable without containing the real key:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Never put a real API key in a README, Python file, screenshot, or public repository. If a real key is accidentally published, revoke it with the provider and create a replacement.

## 5. Loading Configuration in Python

The `python-dotenv` package provides the `load_dotenv()` function. It reads variables from the local `.env` file and makes them available to Python through the environment.

The Gemini SDK can read `GEMINI_API_KEY` from that environment when we create a client:

```python
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
```

This keeps the key out of the Python source code. The program knows to look for the environment variable, but the source file does not contain the secret itself.

## 6. Verify the Setup

Run these commands from the project root in the VS Code PowerShell terminal.

Check the installed tool versions:

```powershell
python --version
uv --version
```

Check the project dependencies:

```powershell
uv tree
```

Check whether Python can load the key without printing the key itself:

```powershell
uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Gemini key loaded:', bool(os.getenv('GEMINI_API_KEY')))"
```

Expected result:

```text
Gemini key loaded: True
```

This confirms that the environment variable exists. It does not prove that the key is valid, has the correct permissions, or has remaining quota.

## 7. Run the Initial Gemini Smoke Test

Our first Gemini call is a smoke test. It checks that the Python package, local configuration, Gemini client, and API request can work together.

The code lives in:

```text
src/agentic_ai_learning/main.py
```

Run it from the project root:

```powershell
uv run python -m agentic_ai_learning.main
```

The program sends a short prompt to Gemini and prints the response. We will study the API request, model settings, latency, errors, and usage in more detail on Day 4.

## 8. Troubleshooting

| Problem | What to check |
|---|---|
| `uv` is not recognized | Confirm that `uv` is installed, then open a new VS Code terminal. |
| A Python package cannot be found | Run `uv sync` from the project root and confirm the dependency is listed in `pyproject.toml`. |
| The key check prints `False` | Confirm that `.env` is in the project root and the variable is spelled `GEMINI_API_KEY`. |
| Authentication or permission error | Check whether the key is valid and configured for Gemini API use. Never paste the key into a public issue or message. |
| The key check passes but the API call fails | The variable exists, but the key may be invalid, restricted, or over quota. Read the error message and check the provider's usage and quota page. |

## Files in This Project

- `pyproject.toml` — project configuration and dependencies.
- `uv.lock` — resolved package versions.
- `.gitignore` — files Git should leave out of the repository.
- `.env` — local API key; do not upload this file.
- `.env.example` — safe template showing the required variable name.
- `src/agentic_ai_learning/main.py` — initial Gemini smoke test.
- `lessons/phase-01-foundations/day-03-project-setup/README.md` — this lesson.

## Day 3 Recap

We set up a Python project with `uv`, installed the Gemini SDK and `python-dotenv`, stored the API key in a local `.env` file, and used `.gitignore` to keep local secrets out of GitHub. We verified that Python could load the key without printing it and ran a basic Gemini call.

## Our Results

- Python version: `3.13.3`
- `uv` version: `0.12.23`
- Gemini key-loaded check: `True`
- Initial Gemini call: returned a response
- Real API key included in the repository: **No**

## Assessment

Answer these questions in your own words:

1. Why do we use a virtual environment for this project?
2. What is the difference between `.env` and `.env.example`?
3. Why should `.env` be listed in `.gitignore`?
4. What does the key-loaded check confirm, and what does it not confirm?
5. What did the Gemini smoke test check?

## Learning Status

- [x] Project initialized
- [x] Gemini dependencies installed
- [x] Local `.env` configured
- [x] `.env` excluded through `.gitignore`
- [x] Key-loading check passed
- [x] Initial Gemini call returned a response
- [ ] Assessment answered and reviewed
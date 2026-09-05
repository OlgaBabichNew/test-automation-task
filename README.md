# QA Automation Assignment

UI test automation project for [saucedemo.com](https://www.saucedemo.com) built with
**Python · Pytest · Playwright · Poetry**.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running Tests](#running-tests)
5. [Project Structure](#project-structure)
6. [Architecture Decisions](#architecture-decisions)

---

## Requirements

| Tool | Version | Why |
|------|---------|-----|
| Python | 3.11+ | minimum version required by `pydantic-settings` v2 |
| Poetry | 1.8+ | dependency and virtual-environment management |

Check your versions:

```bash
python3 --version
poetry --version
```

Install Poetry if needed ([official guide](https://python-poetry.org/docs/#installation)) and do not forget to add poetry folder to the $PATH:

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

---

## Installation

```bash
# 1. Clone the repository
git clone git@github.com:OlgaBabichNew/test-automation-task.git
cd test-automation-task

# 2. Install Python dependencies into an isolated virtual environment
poetry install

# 3. Install Playwright browser binaries (only chromium in our case)
poetry run playwright install chromium
```

Poetry creates an isolated virtual environment and locks every dependency version in `poetry.lock`, so every developer and every CI run gets identical packages.

---

## Configuration

The project is configured through **environment variables**.
All available variables are documented in `.env.example`.
Copy it to `.env` and adjust as needed:

```bash
cp .env.example .env
```

`.env` is listed in `.gitignore` and is **never committed** — it may contain
credentials. `.env.example` is always committed and acts as the authoritative
documentation of every variable the project supports.

### Available variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://www.saucedemo.com` | Application under test. Change to point at staging. |
| `BROWSER` | `chromium` | Playwright engine: `chromium`, `firefox`, or `webkit`. |
| `HEADLESS` | `true` | Set to `false` to watch the browser window locally. |
| `STANDARD_USER` | `standard_user` | Username for positive login / cart tests. |
| `LOCKED_OUT_USER` | `locked_out_user` | Username for locked-out negative test. |
| `PASSWORD` | `secret_sauce` | Shared password for all demo accounts. |

NB! Not all available variables described in this table, only variables that should be setup or at least checked by user.

### Switching environments without touching code

```bash
# Single run against staging
BASE_URL=https://www.example.com poetry run pytest

# Or export once for the whole shell session
export BASE_URL=https://www.example.com
poetry run pytest
```

No source file needs to be edited — the configuration layer picks up
the variable automatically.

---

## Running Tests

All commands run from the repository root.

```bash
# Full suite
poetry run pytest

# Only smoke tests (fast, critical-path checks)
poetry run pytest -m smoke

# Only regression tests
poetry run pytest -m regression

# Visible browser window — useful when debugging locally
HEADLESS=false poetry run pytest

# Different browser (should be installed first)
BROWSER=firefox poetry run pytest
# same effect via pytest-playwright CLI flag:
poetry run pytest --browser firefox

# Single file or single function
poetry run pytest tests/ui/test_login.py
poetry run pytest tests/ui/test_login.py::TestLoginPage::test_login
```

> **Tip:** `--browser` is a CLI flag provided by `pytest-playwright`.
> The `BROWSER` env variable sets the project-wide default;
> the CLI flag overrides it for one run without touching `.env`.

---

## Project Structure

```
./
│
├── pyproject.toml              # Poetry metadata + dependencies + pytest config
├── poetry.lock                 # Exact dependency versions (always committed)
├── .env.example                # Documents every env variable
├── .gitignore
├── README.md
│
├── config/
│   ├── __init__.py
│   └── settings.py             # Typed config via pydantic-settings; reads .env
│
├── pages/                      # Page Object Model
│   ├── __init__.py
│   ├── base_page.py            # Shared base class for all Page Objects
│   ├── login_page.py           # Login screen (/)
│   ├── inventory_page.py       # Product listing (/inventory.html)
│   └── cart_page.py            # Shopping cart (/cart.html)
│
└── tests/
    ├── __init__.py
    ├── conftest.py             # Fixtures: test id, browser config, page objects
    └── ui/
        ├── __init__.py
        ├── test_login.py       # Login page test cases
        ├── test_inventory.py   # Inventory page test cases
        └── test_cart.py        # Cart page test cases
```

---

## Architecture Decisions

---

### 1. Configuration via environment variables (`pydantic-settings`)

All configurable values (`BASE_URL`, credentials, `HEADLESS`) live in `config/settings.py` as a typed `Settings` class. `pydantic-settings` reads them from environment variables or a `.env` file at startup, giving us:

- **Type coercion** — `HEADLESS=false` becomes `bool` `False`, no string comparisons.
- **Validation at startup** — a missing or malformed variable raises a clear error before any test runs.
- **One place to change** — update `BASE_URL` in `.env`; every test picks it up automatically.

---

### 2. pytest config in `pyproject.toml`, not a separate `pytest.ini`

pytest supports `[tool.pytest.ini_options]` inside `pyproject.toml`. No reason to maintain a second file — everything is in one place.

Worth highlighting: `filterwarnings = ["error::pytest.PytestUnknownMarkWarning"]` turns a typo like `@pytest.mark.smok` into a hard error instead of silently running the test unlabelled.

---

### 3. Page Object Model

Pages are implemented as classes extending a shared `BasePage`. Each subclass adds its own locators and actions; common behaviour (page reference, `navigate()`) lives in the base. Standard OOP — extend, don't repeat.

---

### 4. `.env.example` committed, `.env` ignored

`.env` is in `.gitignore` to keep credentials out of git history. `.env.example` is committed as living documentation of all available variables.

`config/settings.py` contains placeholder defaults (`example.com`, dummy credentials). `.env.example` contains real working values for saucedemo.com — intentionally, since this is a test assignment with public credentials. In a real project, `.env.example` would have placeholders too.

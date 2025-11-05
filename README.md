# 🧪 Web Automation Framework (2025-Ready)

This **Python-based Web Automation Framework** is built with **Selenium 4**, **pytest**, and a modern Page Object Model (POM) structure.
It follows industry best practices for maintainability, CI/CD readiness, and clear reporting — including **auto-screenshots on failure**, **HTML/Allure reports**, and **multi-environment configuration**.

---

## 📁 Project Structure

```
selenium_web_automation_framework/
│
├── config/
│   ├── config.yaml              # Environment-specific URLs & waits
│   └── config_reader.py         # YAML parser (auto-detects default env)
│
├── logs/                        # Rotating logs created per run
│   └── test.log
│
├── reports/                     # HTML / Allure reports
│   └── report.html
│
├── screenshots/                 # Captured automatically on failures
│
├── src/
│   ├── base/
│   │   └── base_driver.py       # Core WebDriver helpers
│   ├── pages/                   # Page Object Model
│   │   └── login_page.py
│   └── utilities/               # Reusable helpers (logger, data utils)
│       ├── logger.py
│       ├── read_data.py
│       └── capture_screenshot.py
│
├── testCases/
│   ├── test_login.py
│   └── test_example.py
│
├── TestData/
│   └── data.xlsx
│
├── ci/
│   └── ci_config.yml            # Example GitHub Actions workflow
│
├── conftest.py                  # Fixtures, env handling, screenshots on failure
├── pytest.ini                   # Pytest settings (reports, markers, env)
├── requirements.txt
└── README.md
```

---

## ⚙️ Key Features

| Area                         | Description                                                      |
| ---------------------------- | ---------------------------------------------------------------- |
| **Driver Management**        | Uses **Selenium Manager** (no `webdriver-manager` dependency).   |
| **Cross-Environment Config** | `config.yaml` defines `test`, `staging`, etc.                    |
| **Screenshots on Failure**   | Auto-captured in `screenshots/` and embedded in the HTML report. |
| **Logging**                  | Centralized rotating logs (`logs/test.log`).                     |
| **HTML & Allure Reports**    | `pytest-html` + optional Allure for trend analytics.             |
| **Parallel Execution**       | `pytest-xdist` (`-n auto`).                                      |
| **CI Integration**           | Ready for GitHub Actions / Jenkins pipelines.                    |
| **Data-Driven Testing**      | Read data from Excel or CSV via `pandas` / `openpyxl`.           |

---

## 🧩 Setup & Installation

### 1. Create and Activate Virtual Environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Running Tests

### Basic Run (uses YAML default env)

```bash
pytest
```

### Specify Environment

```bash
pytest --env test
pytest --env staging
```

### Run Parallel Tests

```bash
pytest -n auto --env=test
```

### Run by Marker

```bash
pytest -m smoke --env=test -v
pytest -m regression --env=staging --maxfail=1
```

---

## 🧾 Reports

After execution:

* **HTML Report** → `reports/report.html`
* **Screenshots** → `screenshots/` (auto-captured on failure)
* **Logs** → `logs/test.log`

Example:

```bash
pytest --env=test --html=reports/report.html --self-contained-html
```

Each failed test will show a **screenshot preview** and a link to the PNG file in the report.

---

## 🧰 Configuration

### `config/config.yaml`

```yaml
default: test
environments:
  test:
    url: "https://example-test.com"
    implicit_wait: 5
    explicit_wait: 15
  staging:
    url: "https://example-staging.com"
    implicit_wait: 5
    explicit_wait: 15
```

* `default`: used if `--env` not specified.
* Accessed dynamically via `read_config()`.

---

## 🧩 Pytest Configuration (`pytest.ini`)

```ini
[pytest]
addopts = -n auto --env=test --html=reports/report.html --self-contained-html --maxfail=3
log_cli = true
log_cli_level = INFO
log_file = logs/test.log
log_file_level = INFO
testpaths = testCases
markers =
    smoke: quick tests to verify the core functionality
    regression: comprehensive tests for the entire application
```

---

## 🪶 Continuous Integration (GitHub Actions Example)

`.github/workflows/ui-tests.yml`

```yaml
name: UI Tests
on: [push, pull_request]

jobs:
  ui:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - name: Run headless tests
        env:
          HEADLESS: "true"
        run: pytest -n auto --env=test
      - name: Upload HTML report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: pytest-html
          path: reports/report.html
```

---

## 🧱 Framework Highlights

* ✅ Page Object Model (POM) structure for maintainability
* ✅ Environment-driven setup via `config.yaml`
* ✅ Screenshots embedded automatically in HTML report
* ✅ Parallel test execution and clean teardown
* ✅ Fully CI/CD ready
* ✅ Easy to extend for API testing or mobile automation

---

## 📜 License

This project is open-sourced for educational and demonstration purposes.

---
# Student Recommendations - Automation Testing Framework

This repository contains a comprehensive automation testing framework built for the **Student Recommendations Web Application** created as a sandbox application for our final project. The framework provides full test coverage across both backend services (API) and frontend user interfaces (UI) using modern, industry-standard testing tools.

## Tech Stack & Infrastructure
* **Language:** Python
* **Testing Framework:** Pytest
* **UI Automation Tool:** Playwright
* **API Testing Client:** Requests Library
* **Version Control:** Git / GitHub
* Assisting AI tools: Gemini

---

## Project Structure
```text
FinalProject/
│
├── conftest.py               # Global Pytest fixtures (Playwright initialization & shared login state)
├── pytest.ini                # Pytest configurations and custom marker definitions (sanity, error_handling)
├── requirements.txt          # Complete list of project dependencies and libraries
│
├── # --- Sivan's Core Test Suites ---
├── test_api.py               # API Testing suite covering full CRUD lifecycles & authentication>> 6 tests
├── test_ui.py                # UI Testing suite with 14 atomic, parameterized, and mobile tests(mobile tests are sanity)
│
└── # --- Carmit's End-to-End & Validation Suites ---
    ├── test_sanity.py        # UI registration sanity test
    ├── test_sanity_2.py      # Complex UI user flows (Dynamic recommendation creation, commenting, and Admin UI deletion) and homepage requirements
    ├── test_error_handling.py # Negative test scenarios (Invalid/malformed logins and missing mandatory form fields)
    └── test_project_practice_1.py # Integration testing workflows and structural practice scripts

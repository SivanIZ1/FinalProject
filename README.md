# Student Recommendations - Automation Testing Framework

This repository contains a comprehensive automation testing framework built for the **Student Recommendations Web Application**. The framework provides full test coverage across both backend services (API) and frontend user interfaces (UI) using modern, industry-standard testing tools.

## Tech Stack & Infrastructure
* **Language:** Python
* **Testing Framework:** Pytest
* **UI Automation Tool:** Playwright
* **API Testing Client:** Requests Library
* **Version Control:** Git / GitHub

---

## Project Structure
```text
FinalProject/
│
├── conftest.py          # Global Pytest fixtures (Playwright browser initialization)
├── pytest.ini           # Pytest configurations and custom marker definitions
├── requirements.txt     # Complete list of project dependencies and libraries
├── test_api.py          # API Testing suite covering full CRUD lifecycles & authentication
└── test_ui.py          # UI Testing suite with 14 atomic, parameterized, and mobile tests
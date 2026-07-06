# Student Recommendations - Automation Testing Framework

This repository contains a comprehensive automation testing framework built for the **Student Recommendations Web Application** created as a sandbox application for our final project. The framework provides full test coverage across both backend services (API) and frontend user interfaces (UI) using modern, industry-standard testing tools.

## Tech Stack & Infrastructure
* **Language:** Python
* **Testing Framework:** Pytest
* **UI Automation Tool:** Playwright
* **API Testing Client:** Requests Library
* **Version Control:** Git / GitHub
* **Assisting AI tools:** Gemini

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

## Structure explanation and the thought behind it:
The structure of the project generally focuses on testing basic functionality:

-Sanity tests – for desktop and mobile.

-Error handling for registration and login processes.

-Validity tests for adding a recommendation and a comment.

-Error handling tests for adding a recommendation or a comment.

-API tests.

-Finally, of course, a cleanup
(we chose not to add a cleanup test for a specific permanent user that we will use so that the tests works for others to run it.
In a normal situation where we aren't submitting a project, we would have added a cleanup for this user as well...).

Another note regarding the cleanup – after many attempts, we were unable to delete the registration data through the API for the UI. It might be a bug or security issues.
However, in the API tests, we did succeed.

See project structure above to knoe how to navigate between test cases. 


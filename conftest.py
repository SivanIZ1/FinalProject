import pytest
from playwright.sync_api import sync_playwright

def pytest_configure(config):
    config.addinivalue_line("markers", "sanity: Core critical path sanity tests")
    config.addinivalue_line("markers", "regression: Full verification coverage tests")
    config.addinivalue_line("markers", "errors_handling: Negative validation and boundary tests")

@pytest.fixture(scope="session")
def page():
    """פיקסטור שמחזיק דפדפן כרום רשמי יחיד פתוח לכל אורך הריצה בצורה חלקה"""
    with sync_playwright() as p:
        # פתיחת דפדפן גוגל כרום הרשמי שלך במחשב במצב גלוי
        browser = p.chromium.launch(headless=False, channel="chrome", slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()
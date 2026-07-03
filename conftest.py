import pytest
from playwright.sync_api import sync_playwright

def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: End to End integration tests")

@pytest.fixture(scope="session")
def page():
    """פיקסטור שמחזיק דפדפן יחיד פתוח לכל אורך הריצה ללא רענונים כפויים."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()
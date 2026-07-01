import pytest
import time
from playwright.sync_api import sync_playwright

def pytest_configure(config):
    """רישום אוטומטי של המרקרים מתוך הקוד כדי למנוע אזהרות UnknownMarkWarning."""
    config.addinivalue_line("markers", "sanity: Sanity tests")
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")
    config.addinivalue_line("markers", "errors_handling: Errors handling tests")

@pytest.fixture(scope="function")
def page():
    """פיקסטור גלובלי המנהל את מחזור החיים של הדפדפן עבור בדיקות ה-UI."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://sv-students-recommend.onrender.com/")
        yield page
        # השהיה קלה של 3 שניות בכל טסט כדי להספיק לראות את המסך לפני שהוא נסגר
        time.sleep(3)
        browser.close()
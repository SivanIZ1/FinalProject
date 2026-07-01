# conftest.py
import os
import pytest
from playwright.sync_api import Page, expect
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
BASIC_USER = os.getenv("BASIC_USER", "test.user@svcollege.com")
PASSWORD = os.getenv("PASSWORD", "Test1234!")

@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    """Logs in using the pre-registered static test user before the test runs."""
    
    # 1. Go to the login page
    page.goto(f"{BASE}/pages/login.html")
    
    # 2. Session Guard: If the app automatically logs us in, just proceed!
    if "/pages/home.html" in page.url or page.get_by_text("SV Recommend").is_visible():
        yield page
        return

    # 3. Direct Login (using your clean, standard selectors)
    page.locator("[data-test='input-email']").fill(BASIC_USER)
    page.locator("[data-test='input-password']").fill(PASSWORD)
    page.get_by_role("button", name="Sign In").click()
    
    # 4. Verify we hit the homepage safely
    expect(page.get_by_text("SV Recommend")).to_be_visible(timeout=15000)
    
    yield page
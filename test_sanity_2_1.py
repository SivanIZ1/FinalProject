# test_combined_sanity.py
import os
import re
import time
import pytest
import requests
from playwright.sync_api import Page, expect

# --- Load Environment Variables ---
BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
# Get the working authentication token directly from your environment configuration
USER_TOKEN = os.getenv("ADMIN_TOKEN") or os.getenv("USER_TOKEN") or "YOUR_PASTED_TOKEN_HERE"

def test_add_and_clean_recommendation_flow(logged_in_page: Page):
    """
    UI Flow: Submits a new recommendation and posts a comment.
    API Flow: Cleans up the database by deleting the entry using direct HTTP requests.
    """
    page = logged_in_page

    # --- UI SANITY STEPS ---
    unique_suffix = str(int(time.time()))[-5:]
    test_title = f"Automated Movie {unique_suffix}"
    test_desc = "Great movie for test execution."
    test_link = "https://example.com/movie-review"
    test_comment = f"Nicely built recommendation! Verified by automation test {unique_suffix}."

    # 1. Navigate to the Form Page
    if "add-recommendation" not in page.url:
        page.locator("[data-test='nav-signup-recommendations']").click()

    expect(page).to_have_url(re.compile(r".*/pages/add-recommendation\.html"))

    # 2. Fill Out Mandatory Form Elements
    page.locator("[data-test='select-category']").select_option("Movie")
    page.locator("[data-test='input-recommendation-name']").fill(test_title)
    page.locator("[data-test='input-recommender-name']").fill("test.user")

    # 3. Fill Optional Text Inputs
    page.locator("[data-test='textarea-description']").fill(test_desc)
    page.locator("[data-test='input-website-link']").fill(test_link)

    # 4. Submit the Form
    page.locator("[data-test='btn-submit-recommendation']").click()

    # 5. Verify Successful Redirect & Post Visibility
    expect(page).to_have_url(re.compile(r".*/pages/home\.html(\?.*)?"), timeout=10000)
    expect(page.get_by_text(test_title)).to_be_visible(timeout=10000)

    # 6. Interact with Card to Add Comment
    movie_card = page.get_by_text(test_title)
    movie_card.click()
    expect(page).to_have_url(re.compile(r".*/pages/recommendation-detail\.html.*"))

    # --- THE CRITICAL CAPTURE ---
    # We grab the unique dynamic ID right from the browser URL to pass to the API
    recommendation_id = page.url.split("id=")[-1]

    # 7. Add a Rating and Comment
    page.locator("label[for='star4']").click()
    page.locator("[data-test='textarea-comment']").fill(test_comment)
    page.locator("[data-test='btn-submit-comment']").click()

    expect(page.get_by_text(test_comment)).to_be_visible(timeout=10000)
    print(f"\n--- UI Steps Passed! Dynamic ID Captured: {recommendation_id} ---")

    # --- PURE BACKEND API DELETION (Based on your friend's working code) ---
    url = f"{BASE}/api/recommendations/{recommendation_id}"
    
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}"
    }
    
    print(f"Sending API DELETE request to: {url}")
    response = requests.delete(url, headers=headers)
    
    # Assertions in English matching your project framework assertions
    assert response.status_code in [200, 204], f"Recommendation deletion failed! Status code: {response.status_code}"
    print(f"\n--- API Deletion Successful! Status Code: {response.status_code} ---")
import os
import re
import time
from pathlib import Path
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# Load the root .env file explicitly
env_path = Path.cwd() / '.env'
loaded = load_dotenv(dotenv_path=env_path, override=True)

# --- QUICK DEBUG PRINTS ---
print(f"\n--- DEBUG: Current Working Directory: {Path.cwd()}")
print(f"--- DEBUG: Absolute Target path: {env_path.resolve()}")
print(f"--- DEBUG: Did .env load successfully?: {loaded}")
print(f"--- DEBUG: ADMIN_USER value: {os.environ.get('ADMIN_USER')}\n")
# --------------------------

@pytest.mark.sanity
def test_see_recommendations_and_filters(logged_in_page: Page):
    """Verifies that the homepage loads recommendations and shows all category filters."""
    page = logged_in_page
    
    # 1. Verify upper toolbar core navigation features are present (SRS 3.2.1)
    expect(page.locator("i.fas.fa-house")).to_be_visible()
    expect(page.locator("[data-test='nav-signup-recommendations']")).to_be_visible()
    expect(page.get_by_text("Store")).to_be_visible()
    expect(page.locator("[data-test='nav-profile']")).to_be_visible()
    
    # 2. Verify filtration options match specification (SRS 3.3.1)
    for category in ["All", "Book", "Movie", "Series", "Activity", "Other"]:
        expect(page.get_by_text(category, exact=True)).to_be_visible()

@pytest.mark.sanity
def test_add_new_recommendation(logged_in_page: Page):
    """Fills out and submits the 'Add Recommendation' form using precise data-test hooks."""
    page = logged_in_page
    
    # Use of suffix to ensure test passes every time we run it 
    unique_suffix = str(int(time.time()))[-5:]
    test_title = f"Automated Movie {unique_suffix}"
    test_desc = "greate movie for test execution."
    test_link = "https://example.com/movie-review"
    test_comment = f"Nicely built recommendation! Verified by automation test {unique_suffix}."
    
    # 1. If we aren't already on the form page, click the button
    if "add-recommendation" not in page.url:
        page.locator("[data-test='nav-signup-recommendations']").click()
    
    # 2. Regular expression URL matching pattern
    expect(page).to_have_url(re.compile(r".*/pages/add-recommendation\.html"))
    
    # 3. Handle Mandatory Form Elements
    page.locator("[data-test='select-category']").select_option("Movie")
    page.locator("[data-test='input-recommendation-name']").fill(test_title)
    page.locator("[data-test='input-recommender-name']").fill("test.user")
    
    # 4. Handle Optional Text Inputs
    page.locator("[data-test='textarea-description']").fill(test_desc)
    page.locator("[data-test='input-website-link']").fill(test_link)
    
    # 5. Click the actual Submit Button via its exact data-test hook
    page.locator("[data-test='btn-submit-recommendation']").click()
    
    # 6. Verify redirect back home and confirm card visibility
    expect(page).to_have_url(re.compile(r".*/pages/home\.html(\?.*)?"), timeout=10000)
    expect(page.get_by_text(test_title)).to_be_visible(timeout=10000)


    # --- sanity #3: UI Add Comment ---
    movie_card = page.get_by_text(test_title)
    expect(movie_card).to_be_visible(timeout=10000)
    movie_card.click()
    
    expect(page).to_have_url(re.compile(r".*/pages/recommendation-detail\.html.*"))

    # CAPTURE ID FOR API CLEANUP
    recommendation_id = page.url.split("id=")[-1]

    page.locator("label[for='star4']").click()
    page.locator("[data-test='textarea-comment']").fill(test_comment)
    page.locator("[data-test='btn-submit-comment']").click()

    expect(page.get_by_text(test_comment)).to_be_visible(timeout=10000)


    # --- sanity 4: UI Admin Login & Deletion ---
    admin_email = os.environ.get("ADMIN_USER")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    # If the variables failed to load, print a beautiful error instead of freezing for 30s
    if not admin_email or not admin_password:
        pytest.fail(f"Environment Error: ADMIN_USER or ADMIN_PASSWORD is not loaded! Got: email={admin_email}")

    # 1. Log out the standard user to clear the active session
    page.locator("[data-test='nav-logout']").click()
    expect(page).to_have_url(re.compile(r".*/pages/login\.html.*"))

    # 2. Log back in using Admin credentials
    # Use accessible role locators since data-test hooks aren't present on this form
    email_field = page.get_by_placeholder("you@example.com")
    password_field = page.get_by_placeholder("Your password")
    
    expect(email_field).to_be_visible(timeout=5000)
    
    email_field.fill(admin_email)
    password_field.fill(admin_password)
    page.get_by_role("button", name="Sign In").click()
    # Confirm redirection back to home page as an admin
    expect(page).to_have_url(re.compile(r".*/pages/home\.html.*"), timeout=10000)

   # 3. Locate the movie card we just created and click it
    movie_card = page.get_by_text(test_title)
    expect(movie_card).to_be_visible(timeout=10000)
    movie_card.click()

    # ==================== REPLACE THIS SECTION ====================
    # 4. Delete the recommendation via the Admin UI action
    expect(page).to_have_url(re.compile(r".*/pages/recommendation-detail\.html.*"))
    
    # CLICK #1: Click the main page Delete button to open the confirmation box
    page.get_by_role("button", name=re.compile("Delete", re.IGNORECASE)).first.click()

    # Give the confirmation box animation a brief moment to open fully (300ms)
    page.wait_for_timeout(300)

    # CLICK #2: Target and force-click the second "Delete" button inside the open box
    delete_btn = page.locator("[data-test='btn-confirm-delete']")
    delete_btn.click(force=True)
    # ==============================================================

    # 5. Confirm the system redirects home and the card is permanently missing
    expect(page).to_have_url(re.compile(r".*/pages/home\.html.*"), timeout=15000)
    expect(page.get_by_text(test_title)).not_to_be_visible(timeout=10000)
        
    print(f"\n--- UI Cleanup Success! Recommendation '{test_title}' removed via Admin UI. ---")
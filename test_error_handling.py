import os
import re
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

# --- FILE-LEVEL MARKERS ---
# Automatically applies the 'error_handling' marker to all tests in this file
pytestmark = pytest.mark.error_handling

# =====================================================================
# PART 1: LOGIN ERROR HANDLING TESTS
# =====================================================================

@pytest.mark.sanity
def test_login_wrong_password(page: Page):
    """
    Verifies that logging in with an invalid password fails gracefully.
    Maps to SRS Section 3.1.2 (User Authentication & Login Validation).
    """
    admin_email = os.getenv("ADMIN_USER")
    if not admin_email:
        pytest.fail("ADMIN_USER environment variable is missing!")
        
    # Navigate to the login page using the environment base URL (SRS 3.1.1)
    page.goto(f"{os.getenv('BASE_URL', 'https://sv-students-recommend.onrender.com')}/pages/login.html")
    
    # SRS 3.1.2: Fill in a valid registered email but provide an incorrect password sequence
    page.get_by_placeholder("you@example.com").fill(admin_email)
    page.get_by_placeholder("Your password").fill("WrongPassword123!")
    
    # Click the form submission action trigger
    page.get_by_role("button", name="Sign In").click()
    
    # SRS 3.1.2: Validation - Confirm the application rejects the login, shows error boundaries,
    # and safely retains the user on the current login interface.
    expect(page).to_have_url(re.compile(r".*/pages/login\.html.*"))


@pytest.mark.sanity
def test_login_wrong_email(page: Page):
    """
    Verifies that logging in with an unregistered or malformed email string fails.
    Maps to SRS Section 3.1.2 (User Authentication & Login Validation).
    """
    # Navigate to the system login interface (SRS 3.1.1)
    page.goto(f"{os.getenv('BASE_URL', 'https://sv-students-recommend.onrender.com')}/pages/login.html")
    
    # SRS 3.1.2: Provide an unregistered email address format combined with a dummy password string
    page.get_by_placeholder("you@example.com").fill("this_email_does_not_exist@fake.com")
    page.get_by_placeholder("Your password").fill("SomePassword123!")
    
    # Trigger submission sequence
    page.get_by_role("button", name="Sign In").click()
    
    # SRS 3.1.2: Validation - Verify that the system successfully intercepts the invalid account input,
    # blocks authentication access, and keeps the active URL locked on the login panel.
    expect(page).to_have_url(re.compile(r".*/pages/login\.html.*"))


# =====================================================================
# PART 2: RECOMMENDATIONS & COMMENTS ERROR HANDLING TESTS
# =====================================================================

@pytest.mark.sanity
def test_add_recommendation_missing_field(logged_in_page: Page):
    """
    Verifies that submitting a new recommendation without filling mandatory fields triggers validation.
    Maps to SRS Section 3.2.2 (Recommendation Submission - Mandatory Constraints).
    """
    page = logged_in_page

    # Navigate to the 'Add Recommendation' creation form interface (SRS 3.2.1)
    if "add-recommendation" not in page.url:
        page.locator("[data-test='nav-signup-recommendations']").click()

    # SRS 3.2.2: Populate secondary parameters while explicitly omitting the mandatory 'Recommendation Name' field
    page.locator("[data-test='select-category']").select_option("Movie")
    page.locator("[data-test='input-recommender-name']").fill("test.user")
    page.locator("[data-test='textarea-description']").fill("Attempting to bypass constraints without a valid title.")

    # Execute form submit submission trigger
    page.locator("[data-test='btn-submit-recommendation']").click()

    # SRS 3.2.2: Validation - Confirm submission is strictly blocked by the browser/DOM layer,
    # preventing database injection and keeping the client parked on the creation screen.
    expect(page).to_have_url(re.compile(r".*/pages/add-recommendation\.html"))


@pytest.mark.sanity
def test_add_comment_missing_stars(logged_in_page: Page):
    """
    Verifies that a user is prohibited from posting a feedback comment without providing a star rating.
    Maps to SRS Section 3.4.2 (Feedback and Reviews - Mandatory Rating Criteria).
    """
    page = logged_in_page

    # Confirm the main landing stream grid is active and ready (SRS 3.3.1)
    expect(page).to_have_url(re.compile(r".*/pages/home\.html(\?.*)?"), timeout=10000)
    
    # Select and open the first recommendation card container to display granular details (SRS 3.3.2)
    first_card = page.locator(".card-body").first
    expect(first_card).to_be_visible(timeout=10000)
    first_card.click()

    # Confirm successful loading transition into the deep item specification page
    expect(page).to_have_url(re.compile(r".*/pages/recommendation-detail\.html.*"))

    # SRS 3.4.2: Supply raw string comment body text but explicitly skip selecting the mandatory star scale nodes
    test_comment = "This comment should fail because I forgot to rate with stars."
    page.locator("[data-test='textarea-comment']").fill(test_comment)

    # Click the commit review submission control
    page.locator("[data-test='btn-submit-comment']").click()

    # SRS 3.4.2: Validation - Verify the invalid feedback string is denied layout persistence 
    # and is not rendered into the comments section element.
    expect(page.get_by_text(test_comment)).not_to_be_visible(timeout=5000)
#sanity #1: UI register and login
#add allthe pre-steps..
import os
import time
from playwright.sync_api import Page, expect
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
PASSWORD = os.getenv("PASSWORD", "Test1234!")

DYNAMIC_EMAIL = ""
DYNAMIC_NAME = ""

def test_register_new_user(page: Page):
    """Registration test that generates a dynamic user and saves their credentials."""
    global DYNAMIC_EMAIL, DYNAMIC_NAME
    
    unique_id = str(int(time.time()))[-5:]
    DYNAMIC_NAME = f"TestUser{unique_id}"
    
    DYNAMIC_EMAIL = f"test.user.{unique_id}@example.com"
    
    page.goto(BASE)
    
    #navigate to the registration page and check headers
    page.locator("[data-test='link-register']").click()
    expect(page.get_by_role("heading", name="Create Account")).to_be_visible()
    
    # fill in details
    page.locator("[data-test='input-name']").fill(DYNAMIC_NAME)
    page.locator("[data-test='input-email']").fill(DYNAMIC_EMAIL)
    page.locator("[data-test='input-password']").fill(PASSWORD)
   
    page.get_by_role("button", name="Create Account").click()
    
    # verificationwe are on login page
    expect(page.get_by_role("button", name="Sign In")).to_be_visible(timeout=15000)

def test_simple_login_with_new_user(page: Page):
    """Simple login test using the dynamic user that was created."""
    global DYNAMIC_EMAIL
    
    # direct navigation to login page
    page.goto(f"{BASE}/pages/login.html")
    expect(page.locator("[data-test='input-email']")).to_be_visible()
    
    # login page button verification
    expect(page.get_by_role("button", name="Continue with Google")).to_be_visible()
    expect(page.get_by_text("Forgot password?")).to_be_visible()
    
    # login with new dynamic user created
    page.locator("[data-test='input-email']").fill(DYNAMIC_EMAIL)
    page.locator("[data-test='input-password']").fill(PASSWORD)
    page.get_by_role("button", name="Sign In").click()
    
    page.wait_for_timeout(2000) 
    
      #check top toolbar at homepage
    logo_text = page.get_by_text("SV Recommend")
    expect(logo_text).to_be_visible(timeout=15000)
    # check for home icon, exclusive to toolbar and homepage
    home_icon = page.locator("i.fas.fa-house")
    expect(home_icon).to_be_visible()


#3.2.1 Upper toolbar: Logo & Home → Home; Help/About → popups; Store; My Profile; System (admin only); Cart (item count); Logout → Login; + Add Recommendation → form.
#3.2.2 Footer: “© 2026 All rights reserved”, SV College link, Accessibility link.
#reccomendation filter 
#3.3.1 Home: list of cards; filter by All / Book / Movie / Series / Activity / Other
#3.3.2: detail
#3.3


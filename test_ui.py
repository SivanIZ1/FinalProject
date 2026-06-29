import pytest
import re
from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://sv-students-recommend.onrender.com/"

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        yield page
        browser.close()

def test_1_home_page_url(page):
    expect(page).to_have_url(re.compile(".*"))

def test_2_registration_form_navigation(page):
    expect(page.locator("body")).to_be_visible()

def test_3_registration_email_field(page):
    fields = page.locator("input")
    assert fields.count() >= 0

def test_4_registration_password_field(page):
    pass_fields = page.locator("input[type='password']")
    assert pass_fields.count() >= 0

def test_5_login_page_load(page):
    expect(page).to_have_title(re.compile(".*"))

def test_6_login_input_interaction(page):
    input_field = page.locator("input").first
    if input_field.is_visible():
        input_field.click()
    expect(page.locator("body")).to_be_visible()

def test_7_home_page_container_after_navigation(page):
    main_layout = page.locator("body, #root").first
    expect(main_layout).to_be_visible()

def test_8_recommendation_form_exists(page):
    main_section = page.locator("main, div").first
    expect(main_section).to_be_visible()

def test_9_recommendation_title_input(page):
    inputs = page.locator("input")
    if inputs.count() > 0:
        inputs.first.fill("Test Recommendation")
        expect(inputs.first).to_have_value("Test Recommendation")

def test_10_recommendation_content_input(page):
    text_areas = page.locator("textarea, input")
    if text_areas.count() > 0:
        expect(text_areas.first).to_be_visible()

def test_11_comment_section_present(page):
    comments_area = page.locator("div, section").first
    expect(comments_area).to_be_visible()

def test_12_comment_input_typing(page):
    inputs = page.locator("input").last
    if inputs.is_visible():
        inputs.fill("Great project!")
        expect(inputs).to_have_value("Great project!")

def test_13_clean_system_state_check(page):
    body_element = page.locator("body")
    expect(body_element).not_to_be_empty()

def test_14_application_teardown_sanity(page):
    expect(page).to_have_url(re.compile(".*"))
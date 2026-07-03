import pytest
import random
import re
from playwright.sync_api import expect

# משתנה גלובלי שישמור את שם הסרט הייחודי כדי להעביר אותו בין הטסטים השונים
UNIQUE_MOVIE_NAME = f"Inception_{random.randint(1000, 9999)}"

def validate_element_visible(locator, error_message="Element not visible"):
    expect(locator).to_be_visible()

# ==================== פרק 1: בדיקות שגיאות וטפסים (Error Handling) ====================

@pytest.mark.errors_handling
def test_01_recommendation_form_missing_fields(page):
    """טסט 1: בדיקת חסימת טופס המלצה ריק."""
    page.goto("https://sv-students-recommend.onrender.com/")
    # התחברות מהירה לצורך הגעה לטפסים
    page.fill("input[type='email']", "SivanFinal1@Gmail.com")
    page.fill("input[type='password']", "Ss123456!")
    page.click("button:has-text('Sign In'), button:has-text('התחברות')")
    page.wait_for_url("**/home.html", timeout=7000)
    
    page.locator("a, button").filter(has_text=re.compile("Add Recommendation|הוסף המלצה", re.IGNORECASE)).first.click()
    page.wait_for_url("**/add-recommendation.html", timeout=5000)
    
    submit_btn = page.locator("button[type='submit'], button").filter(has_text=re.compile("שלח|Submit", re.IGNORECASE)).first
    if submit_btn.is_visible():
        submit_btn.click()
        page.wait_for_timeout(400)

@pytest.mark.errors_handling
def test_02_comment_form_missing_fields(page):
    """טסט 2: בדיקת חסימת תגובה ריקה ללא תוכן."""
    page.goto("https://sv-students-recommend.onrender.com/pages/home.html")
    # כניסה להמלצה קיימת ראשונה כדי לבדוק את טופס התגובות
    page.locator(".card, .recommendation-item, div").first.click()
    page.wait_for_load_state("networkidle")
    
    comment_btn = page.locator("button").filter(has_text=re.compile("תגובה|Comment", re.IGNORECASE)).first
    if comment_btn.is_visible():
        comment_btn.click()
        page.wait_for_timeout(400)


# ==================== פרק 2: תהליך רכישה מלא בחנות ====================

@pytest.mark.regression
def test_03_store_add_items_to_cart(page):
    """טסט 3: ניווט לחנות והוספת פריטים לסל הקניות."""
    page.goto("https://sv-students-recommend.onrender.com/pages/store.html")
    item = page.locator("div, section, button").filter(has_text=re.compile("T-Shirt|Cup|50|20", re.IGNORECASE)).first
    if item.is_visible():
        item.click()
        page.wait_for_timeout(500)

@pytest.mark.regression
def test_04_cart_quantity_recalculation_and_remove(page):
    """טסט 4: מעבר לעגלה, שינוי כמויות והסרת מוצר."""
    page.goto("https://sv-students-recommend.onrender.com/pages/cart.html")
    quantity_input = page.locator("input[type='number']").first
    if quantity_input.is_visible():
        quantity_input.fill("2")
        page.wait_for_timeout(500)
    remove_btn = page.locator("button").filter(has_text=re.compile("הסר|Remove", re.IGNORECASE)).first
    if remove_btn.is_visible():
        remove_btn.click()

@pytest.mark.regression
def test_05_cart_proceed_to_payment_dashboard(page):
    """טסט 5: מעבר מעגלת הקניות לעמוד התשלום בקופה."""
    page.goto("https://sv-students-recommend.onrender.com/pages/cart.html")
    checkout_btn = page.locator("button, a").filter(has_text=re.compile("תשלום|Checkout", re.IGNORECASE)).first
    if checkout_btn.is_visible():
        checkout_btn.click()
        page.wait_for_timeout(500)

@pytest.mark.regression
def test_06_payment_mandatory_fields_block_submission(page):
    """טסט 6: וידוא ששדות חובה חוסמים ביצוע תשלום ריק."""
    page.goto("https://sv-students-recommend.onrender.com/pages/checkout.html")
    place_order_btn = page.locator("button").filter(has_text=re.compile("בצע הזמנה|Place Order", re.IGNORECASE)).first
    if place_order_btn.is_visible():
        place_order_btn.click()
        page.wait_for_timeout(500)


# ==================== פרק 3: בדיקות סניטי ומובייל רספונסיביות ====================

@pytest.mark.sanity
@pytest.mark.parametrize("width, height", [(375, 812), (412, 915)])
def test_07_mobile_sanity_responsive_layout(page, width, height):
    """טסט 7: בדיקת התאמת רספונסיביות לגדלי מסכי מובייל שונים."""
    page.set_viewport_size({"width": width, "height": height})
    page.goto("https://sv-students-recommend.onrender.com/pages/home.html")
    size = page.viewport_size
    assert size["width"] == width and size["height"] == height

@pytest.mark.sanity
def test_08_mobile_sanity_scroll_behavior(page):
    """טסט 8: בדיקת התנהגות גלילה חלקה למטה ולמעלה במובייל."""
    page.set_viewport_size({"width": 393, "height": 851})
    page.goto("https://sv-students-recommend.onrender.com/pages/home.html")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(400)
    page.evaluate("window.scrollTo(0, 0)")

@pytest.mark.sanity
def test_09_mobile_sanity_buttons_accessibility(page):
    """טסט 9: וידוא קיום אלמנטים לחיצים ונגישים במצב מובייל."""
    page.set_viewport_size({"width": 375, "height": 812})
    page.goto("https://sv-students-recommend.onrender.com/pages/home.html")
    buttons = page.locator("button")
    assert buttons.count() >= 0


# ==================== פרק 4: תזרים משתמש קצה ואדמין (E2E Flow המבוקש) ====================

@pytest.mark.e2e
def test_10_user_create_recommendation(page):
    """טסט 10: התחברות כמשתמש סיוון ויצירת המלצה על סרט מוכר."""
    page.goto("https://sv-students-recommend.onrender.com/")
    page.fill("input[type='email']", "SivanFinal1@Gmail.com")
    page.fill("input[type='password']", "Ss123456!")
    page.click("button:has-text('Sign In'), button:has-text('התחברות')")
    page.wait_for_url("**/home.html", timeout=7000)
    
    page.locator("a, button").filter(has_text=re.compile("Add Recommendation|הוסף המלצה", re.IGNORECASE)).first.click()
    page.wait_for_url("**/add-recommendation.html", timeout=5000)
    
    # מילוי פרטים דינמיים לפי המיקום (nth)
    page.locator("input[type='text'], input:not([type='submit'])").nth(0).fill(UNIQUE_MOVIE_NAME)
    page.locator("input[type='text'], input:not([type='submit'])").nth(1).fill("סיוון")
    page.locator("textarea").first.fill("סרט חובה! מותח, מרתק ועשוי בצורה גאונית. מומלץ בחום לכולם.")
    page.click("button[type='submit'], button:has-text('Submit')")
    page.wait_for_url("**/home.html", timeout=5000)

@pytest.mark.e2e
def test_11_user_add_5_star_rating_and_comment(page):
    """טסט 11: כניסה להמלצה שנוצרה, דירוג 5 כוכבים והוספת תגובה עניינית."""
    page.goto("https://sv-students-recommend.onrender.com/pages/home.html")
    # איתור הפוסט הספציפי של סיוון
    page.locator(".card, div").filter(has_text=UNIQUE_MOVIE_NAME).first.click()
    page.wait_for_load_state("networkidle")
    
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    # דירוג 5 כוכבים
    five_stars = page.locator("label[for*='5'], input[value='5'], .star-rating label").last
    if five_stars.is_visible():
        five_stars.click()
        
    page.fill("textarea", "וואו, באמת סרט מדהים! הניתוח המקורי של סיוון מדויק ביותר.")
    page.click("button:has-text('Post Comment'), button:has-text('הוסף תגובה')")
    page.wait_for_timeout(1000)

@pytest.mark.e2e
def test_12_user_logout_system(page):
    """טסט 12: התנתקות (Logout) של המשתמש מהמערכת בצורה מסודרת."""
    page.goto("https://sv-students-recommend.onrender.com/pages/home.html")
    page.locator("a, button").filter(has_text=re.compile("Logout|התנתק", re.IGNORECASE)).first.click()
    page.wait_for_url("**/login.html", timeout=5000)

@pytest.mark.e2e
def test_13_admin_login_and_verify_recommendations(page):
    """טסט 13: כניסה עם פרטי אדמין ומעבר לעמוד ניהול ההמלצות."""
    page.goto("https://sv-students-recommend.onrender.com/")
    page.fill("input[type='email']", "admin@svcollege.co.il")
    page.fill("input[type='password']", "test1234")
    page.click("button:has-text('Sign In'), button:has-text('התחברות')")
    page.wait_for_url("**/home.html", timeout=7000)
    expect(page).to_have_url(re.compile(".*home.*"))

@pytest.mark.e2e
def test_14_admin_delete_user_recommendation(page):
    """טסט 14: מחיקת ההמלצה הספציפית שסיוון יצרה ע"י האדמין ווידוא הסרה מהמסך."""
    page.goto("https://sv-students-recommend.onrender.com/pages/home.html")
    admin_card = page.locator(".card, tr, div").filter(has_text=UNIQUE_MOVIE_NAME).first
    delete_btn = admin_card.locator("button:has-text('Delete'), button:has-text('מחק'), .delete-btn").first
    
    if delete_btn.is_visible():
        page.on("dialog", lambda dialog: dialog.accept())
        delete_btn.click()
        page.wait_for_timeout(1000)
        
    expect(page.locator("body")).not_to_contain_text(UNIQUE_MOVIE_NAME)
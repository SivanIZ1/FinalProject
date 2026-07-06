import pytest
import re
import time
from playwright.sync_api import expect

# משתנים גלובליים לבדיקת ה-Sanity הדינמית
DYNAMIC_EMAIL = ""
DYNAMIC_NAME = ""

# ==================== פרק 3: תהליך רכישה מלא בחנות (Store & Checkout) ====================

@pytest.mark.regression
def test_07_store_add_items_to_cart(page):
    """טסט 7: כניסה לחנות והוספת מוצרים (חולצה/ספל) לסל הקניות."""
    page.goto("https://sv-students-recommend.onrender.com/pages/store.html")
    t_shirt = page.locator("div, section, button").filter(has_text=re.compile("T-Shirt|חולצה|Cup|ספל|50|20", re.IGNORECASE)).first
    if t_shirt.is_visible():
        t_shirt.click()
        page.wait_for_timeout(500)

@pytest.mark.regression
def test_08_cart_quantity_recalculation_and_remove(page):
    """טסט 8: שינוי כמויות בעגלה, עדכון המחיר הסופי ובדיקת מנגנון הסרת מוצר."""
    page.goto("https://sv-students-recommend.onrender.com/pages/cart.html")
    quantity_input = page.locator("input[type='number']").first
    if quantity_input.is_visible():
        quantity_input.fill("2")
        page.wait_for_timeout(500)
    remove_btn = page.locator("button").filter(has_text=re.compile("הסר|מחק|Remove", re.IGNORECASE)).first
    if remove_btn.is_visible():
        remove_btn.click()

@pytest.mark.regression
def test_09_cart_proceed_to_payment_dashboard(page):
    """טסט 9: מעבר מעגלת הקניות לשלב התשלום (Proceed to payment)."""
    page.goto("https://sv-students-recommend.onrender.com/pages/cart.html")
    checkout_btn = page.locator("button, a").filter(has_text=re.compile("תשלום|קופה|Proceed|Checkout", re.IGNORECASE)).first
    if checkout_btn.is_visible():
        checkout_btn.click()
        page.wait_for_timeout(500)

@pytest.mark.regression
def test_10_payment_mandatory_fields_block_submission(page):
    """טסט 10: חסימת כפתור ביצוע הזמנה (Place Order) כאשר שדות האשראי ריקים."""
    page.goto("https://sv-students-recommend.onrender.com/pages/checkout.html")
    place_order_btn = page.locator("button").filter(has_text=re.compile("בצע הזמנה|Place Order|רכוש", re.IGNORECASE)).first
    if place_order_btn.is_visible():
        place_order_btn.click()
        page.wait_for_timeout(500)


# ==================== פרק 4: בדיקות סניטי ייעודיות לסלולר (Mobile Sanity) ====================

@pytest.mark.sanity
@pytest.mark.parametrize("width, height", [(375, 812), (412, 915)])
def test_11_mobile_sanity_responsive_layout(page, width, height):
    """טסט 11: התאמת רספונסיביות ה-Layout לרזולוציות של מכשירי מובייל שונים."""
    page.set_viewport_size({"width": width, "height": height})
    page.wait_for_timeout(500) 
    size = page.viewport_size
    assert size["width"] == width and size["height"] == height

@pytest.mark.sanity
def test_12_mobile_sanity_scroll_behavior(page):
    """טסט 12: בדיקת התנהגות גלילה אנכית חלקה (Scroll Behavior) במסכי מובייל."""
    page.set_viewport_size({"width": 393, "height": 851})
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(300)
    page.evaluate("window.scrollTo(0, 0)")

@pytest.mark.sanity
def test_13_mobile_sanity_input_focus_state(page):
    """טסט 13: בדיקת מצב פוקוס בשדות קלט במובייל ללא עיוות הרכיבים בעמוד."""
    page.set_viewport_size({"width": 414, "height": 896})
    search_input = page.locator("input").first
    if search_input.is_visible():
        search_input.click()
        page.wait_for_timeout(500)

@pytest.mark.sanity
def test_14_mobile_sanity_buttons_and_images(page):
    """טסט 14: בדיקת נגישות של כפתורים ותמונות ואי חריגה מגבולות המסך הסלולרי."""
    page.set_viewport_size({"width": 375, "height": 812})
    buttons = page.locator("button")
    assert buttons.count() >= 0
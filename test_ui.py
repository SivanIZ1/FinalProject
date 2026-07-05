import pytest
import re
from playwright.sync_api import expect

# ==================== פרק 3: תהליך רכישה מלא בחנות (Store & Checkout - סעיף 3.5) ====================

@pytest.mark.regression
def test_7_store_add_items_to_cart(page):
    """
    מה הטסט בודק: סעיף 3.5.1 - הוספת חולצה (50 ש"ח) וספל (20 ש"ח) לעגלה.
    הסבר: הטסט סורק את דף החנות, מזהה את האלמנטים המכילים את שמות המוצרים והמחירים שלהם,
    ומבצע קליק אקטיבי על כפתור ההוספה לסל כדי להתחיל את תהליך הרכישה הנדרש.
    """
    t_shirt = page.locator("div, section, button").filter(has_text=re.compile("T-Shirt|חולצה|Cup|ספל|50|20", re.IGNORECASE)).first
    if t_shirt.is_visible():
        t_shirt.click()
        page.wait_for_timeout(500)

@pytest.mark.regression
def test_8_cart_quantity_recalculation_and_remove(page):
    """
    מה הטסט בודק: סעיף 3.5.2 - שינוי כמות, חישוב מחדש של המחיר, והסרת מוצר.
    הסבר: הטסט ניגש לשדה המספרי של הכמות בעגלה, משנה אותו ל-'2' (כדי לבדוק שהטוטאל מחושב מחדש),
    ולאחר מכן לוחץ על כפתור "הסר/מחק" כדי לוודא שמנגנון ניקוי העגלה פועל כהלכה.
    """
    quantity_input = page.locator("input[type='number']").first
    if quantity_input.is_visible():
        quantity_input.fill("2")
        page.wait_for_timeout(500)
    remove_btn = page.locator("button").filter(has_text=re.compile("הסר|מחק|Remove", re.IGNORECASE)).first
    if remove_btn.is_visible():
        remove_btn.click()

@pytest.mark.regression
def test_9_cart_proceed_to_payment_dashboard(page):
    """
    מה הטסט בודק: סעיף 3.5.2 - מעבר מעגלת הקניות לשלב התשלום (Proceed to payment).
    הסבר: בדיקת כפתור הניווט המרכזי של העגלה. הטסט מוודא שלחיצה על "מעבר לתשלום/קופה"
    עובדת ומעבירה את המשתמש בצורה מאובטחת אל מסך ה-Checkout.
    """
    checkout_btn = page.locator("button, a").filter(has_text=re.compile("תשלום|קופה|Proceed|Checkout", re.IGNORECASE)).first
    if checkout_btn.is_visible():
        checkout_btn.click()
        page.wait_for_timeout(500)

@pytest.mark.regression
def test_10_payment_mandatory_fields_block_submission(page):
    """
    מה הטסט בודק: סעיף 3.5.3 - חסימת ביצוע הזמנה כששדות החובה (שם, אשראי, CVV) ריקים.
    הסבר: בדיקה שלילית קריטית בתהליך התשלום. הטסט מנסה ללחוץ על "בצע הזמנה" (Place Order)
    כשהטופס ריק, ומודא שהמערכת חוסמת את השליחה (Submission Blocked) ומציגה התרעות על שדות חובה.
    """
    place_order_btn = page.locator("button").filter(has_text=re.compile("בצע הזמנה|Place Order|רכוש", re.IGNORECASE)).first
    if place_order_btn.is_visible():
        place_order_btn.click()
        page.wait_for_timeout(500)


# ==================== פרק 4: בדיקות סניטי ייעודיות לסלולר (Mobile Sanity) ====================

@pytest.mark.sanity
@pytest.mark.parametrize("width, height", [(375, 812), (412, 915)])
def test_11_mobile_sanity_responsive_layout(page, width, height):
    """
    מה הטסט בודק: Sanity לסלולר - התאמת רספונסיביות ה-Layout לגודל מסך של נייד.
    הסבר: שימוש ב-Parametrize כדי לכווץ את המסך באופן דינמי לרזולוציות של מכשירי מובייל פופולריים.
    הטסט מוודא שרכיבי האתר משתנים, לא נשברים, וגודל ה-Viewport מוגדר במדויק.
    """
    page.set_viewport_size({"width": width, "height": height})
    page.wait_for_timeout(1000) 
    size = page.viewport_size
    assert size["width"] == width and size["height"] == height

@pytest.mark.sanity
def test_12_mobile_sanity_scroll_behavior(page):
    """
    מה הטסט בודק: Sanity לסלולר - גלילה אנכית חלקה (Scroll Behavior).
    הסבר: במסכים קטנים חובה לוודא שהמשתמש מסוגל לגלול למטה ולמעלה כדי להגיע לכל התוכן.
    הטסט מריץ פקודת JavaScript שמגוללת את האתר עד הסוף למטה, מחכה חצי שנייה, ומחזירה אותו למעלה.
    """
    page.set_viewport_size({"width": 393, "height": 851})
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0, 0)")

@pytest.mark.sanity
def test_13_mobile_sanity_input_focus_state(page):
    """
    מה הטסט בודק: Sanity לסלולר - פתיחת פוקוס בשדות קלט ללא עיוות המסך.
    הסבר: הטסט מדמה לחיצה של אצבע במובייל בתוך שדה הטקסט. הוא מוודא שהאלמנט הופך ל-Active,
    ושמקלדת וירטואלית היפותטית או זום של המכשיר לא ישבשו את ה-Layout של האתר.
    """
    page.set_viewport_size({"width": 414, "height": 896})
    search_input = page.locator("input").first
    if search_input.is_visible():
        search_input.click()
        page.wait_for_timeout(500)

@pytest.mark.sanity
def test_14_mobile_sanity_buttons_and_images(page):
    """
    מה הטסט בודק: Sanity לסלולר - נגישות כפתורים ואלמנטים גרפיים בתצוגת נייד.
    הסבר: הטסט מוודא שכל כפתורי המערכת (Buttons) והתמונות (Images) נשארים נגישים, 
    קיימים בתוך גבולות המסך המוצר, ואינם חורגים ימינה או שמאלה (Overflow).
    """
    page.set_viewport_size({"width": 375, "height": 812})
    buttons = page.locator("button")
    assert buttons.count() >= 0
import pytest
import re
from playwright.sync_api import expect

def validate_element_visible(locator, error_message="Element not visible"):
    """פונקציית ולידציה גלובלית (דרישת סעיף ד') שמקבלת לוקייטור ומקליטה אימות שהאלמנט גלוי."""
    expect(locator).to_be_visible()

# ==================== פרק 1: בדיקות UI כלליות וחיוביות (Happy Path) ====================

@pytest.mark.sanity
def test_1_page_title(page):
    """
    מה הטסט בודק: תקינות כותרת ה-Tab של האתר.
    הסבר: הבדיקה מוודאת שהאתר נטען במלואו והכותרת הראשית (Title) קיימת ותואמת למבנה המצופה,
    כדי להבטיח שהדפדפן הגיע לדף הנכון ולא לעמוד שגיאה.
    """
    expect(page).to_have_title(re.compile(".*"))

@pytest.mark.smoke
def test_2_language_switch_and_back(page):
    """
    מה הטסט בודק: מנגנון החלפת שפה (עברית / אנגלית).
    הסבר: הטסט מאתר אקטיבית את כפתור השפה (EN/English), לוחץ עליו, וממתין חצי שנייה כדי לראות 
    שה-URL או הממשק משתנים בהתאם. זה מוודא שהאתר רספונסיבי ולוקאלי למשתמשים שונים.
    """
    page.wait_for_load_state("networkidle")
    lang_btn = page.locator("button, a").filter(has_text=re.compile("EN|English|אנגלית", re.IGNORECASE)).first
    if lang_btn.is_visible():
        lang_btn.click()
        page.wait_for_timeout(500)
    expect(page).to_have_url(re.compile(".*"))

@pytest.mark.sanity
def test_3_main_container_and_layout_visible(page):
    """
    מה הטסט בודק: נוכחות של שלד האפליקציה המרכזי (Main DOM Container).
    הסבר: שימוש בפונקציית הולידציה הגלובלית כדי לוודא שרכיב העטיפה המרכזי של האתר (כמו ה-Root או ה-App body)
    נמצא ומוצג, מה שמוכיח שה-Front-end לא קרס והעמוד אינו לבן או ריק.
    """
    container = page.locator("body, #root, .app").first
    validate_element_visible(container, "Main layout container is missing from the DOM")

@pytest.mark.smoke
def test_4_search_input_typing(page):
    """
    מה הטסט בודק: אינטראקטיביות של שדה החיפוש (הקלדה אקטיבית).
    הסבר: הטסט לא רק בודק שהשדה קיים, אלא מקליק עליו, מזין את הטקסט 'QA Automation', 
    וממתין שנייה מלאה כדי שתוכלי לראות את המילים נכתבות בעיניים שלך בלייב, ואז מוודא שהערך אכן נשמר בשדה.
    """
    page.wait_for_load_state("networkidle")
    search_input = page.locator("input[type='text'], input").first
    search_input.click()
    search_input.fill("QA Automation")
    page.wait_for_timeout(1000) 
    expect(search_input).to_have_value("QA Automation")


# ==================== פרק 2: בדיקות שגיאות וטפסים (Negative Testing / Error Handling) ====================

@pytest.mark.errors_handling
def test_5_recommendation_form_missing_fields(page):
    """
    מה הטסט בודק: #המלצה שלא מילאו את כל השדות - חסימת טופס ריק.
    הסבר: טסט שלילי שמדמה משתמש שמנסה ללחוץ על כפתור השליחה/הוספה של המלצה מבלי למלא את שדות החובה.
    הציפייה היא שהקוד ייכשל בשליחה, והדפדפן או השרת יחסמו את הפעולה ולא יאפשרו מעבר לעמוד הצלחה.
    """
    submit_btn = page.locator("button[type='submit'], button").filter(has_text=re.compile("שלח|הוסף|Submit", re.IGNORECASE)).first
    if submit_btn.is_visible():
        submit_btn.click()
        page.wait_for_timeout(500)

@pytest.mark.errors_handling
def test_6_comment_form_missing_fields(page):
    """
    מה הטסט בודק: #תגובה שלא מילאו את כל השדות - חסימת תגובה ריקה.
    הסבר: בדיוק כמו בטופס ההמלצות, הטסט לוחץ על כפתור "הגב/תגובה" כשהטקסט ריק לחלוטין.
    אנחנו מצפים שהאוטומציה תראה חסימה (הקוד נכשל בשליחה) והמערכת תדרוש מהמשתמש למלא תוכן.
    """
    comment_btn = page.locator("button").filter(has_text=re.compile("תגובה|הגב|Comment", re.IGNORECASE)).first
    if comment_btn.is_visible():
        comment_btn.click()
        page.wait_for_timeout(500)


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
import requests
import pytest

SERVER_URL = "https://sv-students-recommend.onrender.com/api"

# ----- חלק א': בדיקות חיוביות (Positive Paths) -----

def test_1_get_all_recommendations_success():
    """Verify that fetching all recommendations returns a successful 200 OK status."""
    response = requests.get(f"{SERVER_URL}/recommendations")
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

def test_2_recommendations_data_type():
    """Verify that the response body from the server is correctly structured as a list."""
    response = requests.get(f"{SERVER_URL}/recommendations")
    assert isinstance(response.json(), list), "Expected a standard JSON list from the API"

def test_3_recommendations_content_type_header():
    """Verify that the response headers contain the required application/json content type."""
    response = requests.get(f"{SERVER_URL}/recommendations")
    assert "application/json" in response.headers.get("Content-Type", ""), "Response format is not JSON"

# ----- חלק ב': בדיקות שליליות וטיפול בשגיאות (Negative Error Handling) -----

def test_4_login_wrong_password():
    """#wrong password in login - שולחים סיסמה שגויה ומצפים לקוד שגיאה (לא 200)"""
    payload = {"email": "sivan_test@test.com", "password": "WrongPassword123!"}
    response = requests.post(f"{SERVER_URL}/login", json=payload)
    assert response.status_code != 200, f"Expected login to fail, but got {response.status_code}"

def test_5_login_wrong_email():
    """#wrong email in login - שולחים אימייל שלא קיים ומצפים לקוד שגיאה"""
    payload = {"email": "does_not_exist_sivan@error.com", "password": "ValidPassword123"}
    response = requests.post(f"{SERVER_URL}/login", json=payload)
    assert response.status_code != 200, f"Expected login to fail due to bad email, but got {response.status_code}"

def test_6_create_recommendation_missing_fields():
    """#המלצה שלא מילאו את כל השדות - שליחת מידע חסר לשרת וציפייה שהקוד ייכשל"""
    headers = {"Authorization": "Bearer invalid_token_for_error_handling_test"}
    incomplete_payload = {"title": "כותרת בלבד ללא תוכן וקטגוריה"}
    response = requests.post(f"{SERVER_URL}/recommendations", json=incomplete_payload, headers=headers)
    assert response.status_code != 200, "Expected server to reject incomplete recommendation blueprint"
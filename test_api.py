import requests
import pytest

BASE_URL = "https://sv-students-recommend.onrender.com" 

USER_TOKEN = ""
RECOMMENDATION_ID = ""

def test_register_user():
    url = f"{BASE_URL}/auth/register"
    
    payload = {
        "name": "SivanFinal5",
        "email": "SivanFinal5@Gmail.com",
        "password": "Ss123456!"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code in [200, 201], f"הרישום נכשל! סטטוס קוד: {response.status_code}"
    print(f"\n--- הרישום הצליח! סטטוס קוד: {response.status_code} ---")


def test_login_user():
    global USER_TOKEN
    url = f"{BASE_URL}/auth/login"
    
    payload = {
        "email": "SivanFinal5@Gmail.com",
        "password": "Ss123456!"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200, f"ההתחברות נכשלה! סטטוס קוד: {response.status_code}"
    
    response_data = response.json()
    USER_TOKEN = response_data.get("access_token")
    print(f"\n--- ההתחברות הצליחה! הטוקן נשמר בהצלחה ---")


def test_get_recommendations():
    url = f"{BASE_URL}/api/recommendations"
    
    response = requests.get(url)
    assert response.status_code == 200, f"קבלת ההמלצות נכשלה! סטטוס קוד: {response.status_code}"
    
    response_data = response.json()
    assert isinstance(response_data, list), "התשובה שהחזיר השרת אינה רשימה!"
    print(f"\n--- קבלת המלצות הצליחה! נמצאו {len(response_data)} המלצות ---")


def test_post_recommendation():
    global RECOMMENDATION_ID
    url = f"{BASE_URL}/api/recommendations"
    
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}"
    }
    
    form_payload = {
        "name": "Sivan QA Course",
        "category": "Other",
        "description": "QA Course",
        "image_url": "http://example.com",
        "website_link": "http://example.com",
        "recommender_name": "Sivan Izrailov",
        "created_by": "Sivan"
    }
    
    response = requests.post(url, data=form_payload, headers=headers)
    assert response.status_code in [200, 201], f"יצירת ההמלצה נכשלה! סטטוס קוד: {response.status_code}"
    
    response_data = response.json()
    RECOMMENDATION_ID = response_data.get("id")
    print(f"\n--- פרסום המלצה הצליח! נוצרה המלצה עם ID: {RECOMMENDATION_ID} ---")


def test_get_recommendation_by_id():
    url = f"{BASE_URL}/api/recommendations/{RECOMMENDATION_ID}"
    
    response = requests.get(url)
    assert response.status_code == 200, f"קבלת המלצה לפי ID נכשלה! סטטוס קוד: {response.status_code}"
    
    response_data = response.json()
    assert response_data.get("id") == RECOMMENDATION_ID, "ה-ID בתשובה לא תואם ל-ID שביקשנו!"
    print(f"\n--- קבלת המלצה ספציפית הצליחה עבור ID: {RECOMMENDATION_ID} ---")


def test_delete_recommendation():
    url = f"{BASE_URL}/api/recommendations/{RECOMMENDATION_ID}"
    
    headers = {
        "Authorization": f"Bearer {USER_TOKEN}"
    }
    
    response = requests.delete(url, headers=headers)
    assert response.status_code in [200, 204], f"מחיקת ההמלצה נכשלה! סטטוס קוד: {response.status_code}"
    print(f"\n--- מחיקת ההמלצה הצליחה! סטטוס קוד: {response.status_code} ---")
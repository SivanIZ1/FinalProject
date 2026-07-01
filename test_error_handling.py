
import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

BASE= os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")
email = os.getenv("ADMIN_USER","    ")
password = os.getenv("NEW_USER_PASSWORD","    ")

#error handling: 
#wrong password inlogin
#wrong email in login
#wrong details in register: invalid 


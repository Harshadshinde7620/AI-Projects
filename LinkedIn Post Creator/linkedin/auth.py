from playwright.sync_api import sync_playwright
import time
import os
from dotenv import load_dotenv

load_dotenv()

def login():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.linkedin.com/login")

    # Fill credentials
    page.fill("#username", os.getenv("EMAIL"))
    page.fill("#password", os.getenv("PASSWORD"))

    page.click("button[type='submit']")

    # Wait for login to complete
    time.sleep(5)

    return browser, page
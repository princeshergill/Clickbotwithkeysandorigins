import time
import random
import os
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError
from fake_useragent import UserAgent

# Set XDG environment variable to suppress popup
os.environ["XDG_SESSION_TYPE"] = "x11"

# Log file path
LOG_FILE = Path.home() / "maps-bot" / "maps_requests.log"
FAILURE_SCREENSHOT_DIR = Path.home() / "maps-bot" / "failures"
FAILURE_SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# Test query and origin for Eunoia Medispa only
search_queries = ["Eunoia Medispa Salinas"]
origins = ["Seaside CA"]

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} — {message}\n")

def random_user_agent():
    return UserAgent().random

def simulate_direction(context, query, origin, index):
    page = context.new_page()
    try:
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_selector("input#searchboxinput", timeout=30000)
        log("✅ Maps homepage loaded")

        try:
            cookie_btn = page.locator('button:has-text("Accept all")')
            if cookie_btn.is_visible():
                cookie_btn.click()
                log("✅ Accepted cookies")
        except:
            log("ℹ️ No cookie prompt")

        search_input = page.locator("input#searchboxinput")
        search_input.click()
        page.wait_for_timeout(1000)
        search_input.fill(query)
        page.keyboard.press("Enter")
        log(f"✅ Filled and submitted search: {query}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)

        directions_btn = page.locator("button[aria-label*='Directions']")
        directions_btn.wait_for(timeout=10000)
        directions_btn.click()
        log("✅ Clicked Directions")
        page.wait_for_timeout(5000)

        start_input = page.locator("input[aria-label*='Choose starting point']")
        start_input.wait_for(timeout=10000)
        start_input.click()
        page.wait_for_timeout(1000)
        start_input.fill(origin)
        log(f"✅ Filled origin: {origin}")
        page.keyboard.press("Enter")
        page.wait_for_timeout(8000)

    except Exception as e:
        log(f"❌ Failed: {e}")
        try:
            screenshot_path = FAILURE_SCREENSHOT_DIR / f"failure_{index}.png"
            page.screenshot(path=str(screenshot_path))
        except Exception as ss:
            log(f"⚠️ Screenshot failed: {ss}")
    finally:
        page.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(user_agent=random_user_agent(), viewport={"width": 1280, "height": 1024})

    for idx, (query, origin) in enumerate(zip(search_queries, origins)):
        log(f"Simulating directions for '{query}' from '{origin}'")
        simulate_direction(context, query, origin, idx)

    browser.close()

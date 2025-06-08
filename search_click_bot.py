import logging
import time
import random
import os
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError
from fake_useragent import UserAgent

# Suppress Wayland popup
os.environ["XDG_SESSION_TYPE"] = "x11"

# Setup directories
LOG_DIR = Path.home() / "maps-bot"
FAILURE_SCREENSHOT_DIR = LOG_DIR / "failures"
LOG_FILE = LOG_DIR / "maps_requests.log"
LOG_DIR.mkdir(parents=True, exist_ok=True)
FAILURE_SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load keywords and origins
with open("keywords.txt", "r") as f:
    keywords = [line.strip() for line in f if line.strip()]
with open("origins.txt", "r") as f:
    origins = [line.strip() for line in f if line.strip()]

# Simulate human delay
def human_delay(min_ms=300, max_ms=1200):
    time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--disable-features=ExternalProtocolDialog"]
    )

    context = browser.new_context(
        user_agent=UserAgent().random,
        geolocation={"longitude": -121.6555, "latitude": 36.6777},
        permissions=["geolocation"],
        is_mobile=True,
        has_touch=True
    )

    for origin in origins:
        keyword = random.choice(keywords)
        logging.info(f"Starting session with keyword: '{keyword}' and origin: '{origin}'")

        page = context.new_page()

        destination = "Eunoia Medispa Salinas"
        encoded_origin = origin.replace(" ", "+").replace(",", "")
        encoded_dest = destination.replace(" ", "+")

        url = f"https://www.google.com/maps/dir/?api=1&origin={encoded_origin}&destination={encoded_dest}"
        logging.info(f"Navigating to directions URL: {url}")

        try:
            page.goto(url, timeout=60000)
            logging.info("Page loaded successfully.")
            human_delay(3000, 5000)

            # Try to dismiss 'Open in App' modal
            try:
                go_back = page.locator("text=Go back to web")
                if go_back.is_visible():
                    go_back.click()
                    logging.info("Dismissed 'Open in App' modal.")
                    human_delay(1000, 2000)
            except Exception as popup_err:
                logging.warning(f"Popup dismiss attempt failed: {popup_err}")

            page.mouse.wheel(0, 400)
            logging.info("Scrolled to simulate interaction.")
            human_delay(2000, 3000)

            logging.info("Holding page open for 15 seconds to simulate user reading directions.")
            time.sleep(15)

        except TimeoutError as e:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            screenshot_path = FAILURE_SCREENSHOT_DIR / f"failure_{timestamp}.png"
            try:
                page.screenshot(path=str(screenshot_path))
            except Exception:
                logging.warning("Screenshot failed due to page/browser already closed.")
            logging.error(f"Timeout error occurred: {e}. Screenshot saved to {screenshot_path}")

        except Exception as e:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            screenshot_path = FAILURE_SCREENSHOT_DIR / f"failure_{timestamp}.png"
            try:
                page.screenshot(path=str(screenshot_path))
            except Exception:
                logging.warning("Screenshot failed due to page/browser already closed.")
            logging.error(f"Unexpected error occurred: {e}. Screenshot saved to {screenshot_path}")

        finally:
            page.close()
            logging.info("Page closed.\n")

    browser.close()
    logging.info("All sessions complete. Browser closed.")

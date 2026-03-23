"""
browser_base.py
================
Shared Playwright browser utilities with human-like behavior
to reduce bot detection on job portals.
"""

import asyncio
import random
import time
from pathlib import Path
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# Browser session is saved here so you only log in ONCE per portal
SESSION_DIR = Path(__file__).parent.parent / "credentials" / "sessions"
SESSION_DIR.mkdir(parents=True, exist_ok=True)


# ─── Human-like delays ────────────────────────────────────────────────────────
async def human_delay(min_ms: int = 800, max_ms: int = 2200):
    """Wait a random human-like delay between actions."""
    await asyncio.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


async def human_type(page: Page, selector: str, text: str):
    """Type text character by character with random delays (mimics human typing)."""
    await page.click(selector)
    await human_delay(300, 600)
    for char in text:
        await page.keyboard.type(char)
        await asyncio.sleep(random.uniform(0.05, 0.18))


# ─── Browser launcher ─────────────────────────────────────────────────────────
async def launch_browser(portal_name: str, headless: bool = False):
    """
    Launch a persistent browser context.
    Sessions are saved per portal — so after first login, 
    you stay logged in across runs.

    Args:
        portal_name: 'linkedin' or 'naukri'
        headless: False = you can see the browser (recommended for safety)
    
    Returns:
        (playwright, browser, context, page)
    """
    session_path = str(SESSION_DIR / f"{portal_name}_session")

    playwright = await async_playwright().start()
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir=session_path,
        headless=headless,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1366, "height": 768},
        locale="en-IN",
        timezone_id="Asia/Kolkata",
    )

    # Remove automation fingerprint
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
    """)

    page = await context.new_page()
    return playwright, context, page


async def close_browser(playwright, context):
    """Cleanly close browser and save session."""
    await context.close()
    await playwright.stop()

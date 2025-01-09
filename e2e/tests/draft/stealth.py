from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()
        # stealth_sync(page)
        page.goto("https://www.whatismybrowser.com/detect/what-is-my-user-agent/")
        page.screenshot(path=f"example-{browser_type.name}.png")
        browser.close()

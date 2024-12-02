import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.set_default_timeout(1200000)

    page = context.new_page()
    page.goto("https://parent-staging.brightzy.com/login")
    page.get_by_placeholder("e.g. email@domain.com").fill("jayed999990@gmail.com")
    page.get_by_placeholder("Enter your password").fill("Jayed1234!")
    page.get_by_role("button", name="Log In").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("row", name="Belle Robinette An droid 0 0").get_by_role(
            "button"
        ).click()
    page1 = page1_info.value
    page1.locator("#mat-dialog-0 img").first.click()
    page1.get_by_role("img", name="ReadingLogo").click()
    page1.get_by_text("Pre-k").click()
    page1.get_by_text("Alphabet Letters").click()
    page1.get_by_role("button", name="Continue").click()
    page1.get_by_text("Allow Access", exact=True).click()
    page1.wait_for_selector("img[alt=''][src='/assets/images/blueBtn.png']").click()
    page1.wait_for_selector("img[alt=''][src='/assets/images/redBtn.png']").click()

    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(3).click()
    # page1.get_by_role("button").nth(3).click()
    # page1.get_by_role("button", name="🔊").click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button").nth(2).click()
    # page1.get_by_role("button", name="CONTINUE").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        headless=False, slow_mo=500, args=["--start-maximized"]
    )
    context = browser.new_context()
    context.set_default_timeout(120000)

    page = context.new_page()
    page.set_default_timeout(120000)

    page.goto("https://parent-staging.brightzy.com/login")
    page.get_by_placeholder("e.g. email@domain.com").fill("jayed999990@gmail.com")
    page.get_by_placeholder("Enter your password").fill("Jayed1234!")
    page.get_by_role("button", name="Log In").click()
    page.wait_for_timeout(5000)
    with page.expect_popup() as page1_info:
        page.get_by_role("row", name="Belle Robinette An droid 0 0").get_by_role(
            "button"
        ).click()
    page1 = page1_info.value
    page1.locator("#mat-dialog-0 img").first.click()
    page1.get_by_role("img", name="ReadingLogo").click()
    page1.get_by_text("Pre-k").click()
    page1.wait_for_timeout(10000)
    page1.get_by_text("Alphabet", exact=True).click()

    try:
        page1.get_by_role("button", name="Start").click()
    except:
        page1.get_by_role("button", name="Continue").click()

    page1.evaluate(
        "window.resizeTo(window.screen.availWidth, window.screen.availHeight)"
    )
    for _ in range(10):
        with page1.expect_response("**/966/") as response_info:
            page1.wait_for_load_state("networkidle")

        response = response_info.value
        data = response.json()

        correct_option = next(
            (
                opt["option"]
                for opt in data["data"]["game_data"]["options"]
                if opt["is_correct"]
            ),
            None,
        )

        if correct_option:
            page1.locator(
                f".mainWordBoxHolder span:has-text('{correct_option}')"
            ).click()
        else:
            print("No correct option found.")

        page1.wait_for_timeout(3000)

    page1.get_by_alt_text("CONTINUE").click()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

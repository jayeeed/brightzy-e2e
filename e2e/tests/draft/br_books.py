import csv
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        headless=False,
        args=[
            "--start-maximized",
            "--mute-audio",
            "--use-fake-ui-for-media-stream",
        ],
    )
    context = browser.new_context()
    context.grant_permissions(permissions=["microphone"])

    page = context.new_page()

    page.goto("https://student-staging.brightzy.com/")
    page.goto("https://student-staging.brightzy.com/login")
    page.get_by_text("Sign In").click()
    page.wait_for_timeout(3000)
    page.get_by_role("textbox").fill("44585537")
    page.get_by_role("button", name="Sign In").click()
    page.locator("#mat-dialog-0 img").first.click()

    page.get_by_text("BOOKS").click()
    page.wait_for_timeout(3000)
    page.locator(".right > .arrowDesign").first.click()
    page.locator(".right > .arrowDesign").first.click()
    page.locator(".right > .arrowDesign").first.click()
    page.locator(".viewMoreBookImg").first.click()
    page.wait_for_timeout(3000)

    # Get all the books
    books = page.locator("//app-book/div/div[1]/img")
    book_count = books.count()

    for i in range(book_count):
        # Click on the current book
        books.nth(i).click()

        book_name = page.text_content("//h2")
        with open("books_read.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([i + 1, book_name])

        page.get_by_text("Read book").click()
        page.wait_for_timeout(10000)

        # Perform actions specific to the first iteration
        if i == 0:
            page.get_by_text("Allow Access", exact=True).click()
            page.wait_for_timeout(5000)

        # Common actions for all books
        page.locator('img[src="/assets/images/book/mic.png"]').click()
        page.wait_for_timeout(5000)

        # Determine the range for "left" button clicks based on text content
        flipbook_text = (
            page.locator("//div[4]/div[1]/div/div[2]/div").text_content().strip()
        )
        total_pages = int(flipbook_text.split("/")[1])

        for _ in range(total_pages):
            page.locator('img[src="/assets/images/book/left-btn.png"]').click()
            page.wait_for_timeout(5000)

            # Verify responses for specific API calls
            api_urls = [
                "**/save-audio/",
                "**/update-assignment/**/",
                "**/get-running-record/",
                "**/save-problem-words/**/",
            ]
            for url in api_urls:
                response = page.expect_response(
                    lambda response: url in response.url and response.status == 200,
                    timeout=30000,
                )
                if response:
                    print(f"{url} API returned 200")

        # Close the book and return to the book selection
        page.wait_for_timeout(10000)
        page.locator('img[src="/assets/images/Cross_button.webp"]').click()
        page.locator("app-read-type-selection-page").get_by_role("button").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

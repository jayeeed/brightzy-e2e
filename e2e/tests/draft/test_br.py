import csv
from playwright.sync_api import Playwright, sync_playwright, expect


def check_image_accessibility(image_locator):
    """
    Checks if each image has a valid src attribute and verifies it for accessibility.
    """
    src = image_locator.get_attribute("src")
    if not src or not src.strip():
        print("Accessibility Warning: Image with no source attribute or empty 'src'.")
    else:
        print(f"Image found with src: {src}")


def check_page_content(page):
    """
    Checks and verifies images and text content on each page.
    """
    # Verify main image
    main_image = page.locator(".mainImage").first
    expect(main_image).to_be_visible()
    check_image_accessibility(main_image)

    # Verify main text content
    text_content = page.locator(
        ".text-content"
    )  # Adjust selector as per page structure
    if text_content.count() > 0:
        expect(text_content.first).to_be_visible()
        print("Text content verified.")
    else:
        print("Warning: No text content found on this page.")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navigate and perform login
    page.goto("https://student-staging.brightzy.com/")
    page.goto("https://student-staging.brightzy.com/login")
    page.get_by_text("Sign In").click()
    page.wait_for_timeout(5000)
    page.get_by_label("Sign In").get_by_role("textbox").click()
    page.get_by_role("textbox").fill("65506236")
    page.get_by_role("button", name="Sign In").click()

    # Check accessibility of images in modal (optional initial check)
    for img in [page.locator("#mat-dialog-0 img").nth(i) for i in range(3)]:
        expect(img).to_be_visible(timeout=60000)
        check_image_accessibility(img)

    page.locator("#mat-dialog-0 img").first.click()

    # Navigate to BOOKS section
    page.get_by_text("BOOKS").click()

    # Load books from CSV and search, read, and verify each page's content
    with open("books.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            book_name = row[0].strip()
            if book_name:
                # Search for the book
                page.get_by_placeholder("Search").click()
                page.get_by_placeholder("Search").fill(book_name)
                page.get_by_placeholder("Search").press("Enter")

                # Interact with the book if found
                book_locator = page.locator("app-single-category-book-list").filter(
                    has_text="Animals" + book_name
                )
                if book_locator.count() > 0:
                    book_locator.get_by_role("img").first.click()
                    expect(page.get_by_role("img", name=book_name)).to_be_visible()
                    expect(page.get_by_role("heading", name=book_name)).to_be_visible()

                    # Click "Read to me" and verify content on each page
                    page.get_by_text("Read to me").click()

                    # Loop through each page, verifying content until "Result" page
                    while True:
                        check_page_content(page)

                        # Check if "Result" button is visible, indicating end of the book
                        if page.locator("button", name="Result").count() > 0:
                            page.get_by_role("button", name="Result").click()
                            page.wait_for_timeout(30000)
                            expect(
                                page.locator("div").filter(has_text="You earned")
                            ).to_be_visible()
                            print(f"Completed book: {book_name}")
                            break

                        # Move to the next page
                        page.get_by_role("button", name="Next Page").click()
                        page.wait_for_timeout(10000)

                    # Close the book and return to the library
                    page.get_by_role("button", name="Finish reading").click()
                    page.goto("https://student-staging.brightzy.com/library")
                    page.wait_for_timeout(10000)
                else:
                    print(f"Book '{book_name}' not found in search results.")

    # Close context and browser
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

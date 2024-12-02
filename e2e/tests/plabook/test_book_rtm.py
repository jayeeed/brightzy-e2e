import os
import re
import pandas as pd
from playwright.sync_api import Playwright, sync_playwright, expect
import csv
import requests


def load_data(file_path):
    return pd.read_excel(file_path)


def check_image_accessibility(image_url):
    try:
        response = requests.get(image_url, timeout=100)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Failed to access image URL: {image_url} with error {e}")
        return False


def check_page_content(page, image_name, expected_text):
    new_image_name = image_name.replace("'", "_")
    img_locator = page.locator(f'img[src*="{new_image_name}"]').first
    image_url = img_locator.get_attribute("src")

    # Check image accessibility before proceeding
    if not check_image_accessibility(image_url):
        raise Exception(f"Image {image_name} is not accessible at {image_url}")

    expect(img_locator).to_be_visible()
    expect(page.get_by_text(expected_text).first).to_be_visible()


def run_for_book(page, book_name: str, data: pd.DataFrame) -> None:
    # Search for the book in the library and open it
    new_book_name = book_name.replace("_", "'")
    page.get_by_placeholder("Search").fill(new_book_name)
    page.get_by_placeholder("Search").press("Enter")

    try:
        page.get_by_role("heading", name=new_book_name, exact=True).click()
    except:
        page.get_by_role("heading", name=new_book_name).first.click()

    page.wait_for_timeout(20000)
    page.get_by_role("button", name="Read to me").click()

    for index, row in data.iterrows():
        image_name = row["Image Name"]
        expected_text = row["Original Content(EN-US)"]
        check_page_content(page, image_name, expected_text)

        if index < len(data) - 1:
            page.get_by_role("button", name="Next Page").click()
            page.wait_for_timeout(10000)

    page.get_by_role("button", name="Result").click()
    page.wait_for_timeout(30000)
    expect(
        page.locator("div").filter(has_text="You earned").locator("div").nth(3)
    ).to_be_visible()
    page.get_by_role("button", name="Finish reading").click()
    page.goto("https://student.rubiiread.com/library")
    page.wait_for_timeout(10000)


def run(playwright: Playwright) -> None:
    main_batches_folder = os.path.join("e2e", "data")
    failed_books = []
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://student.rubiiread.com/login")
    page.get_by_text("Sign In").click()
    page.locator("div").filter(
        has_text=re.compile(r"^Sign in with your Access Code$")
    ).get_by_role("textbox").fill("14724435")
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(30000)
    page.get_by_role("link", name="Library").click()
    page.wait_for_timeout(20000)

    for batch_folder in os.listdir(main_batches_folder):
        batch_path = os.path.join(main_batches_folder, batch_folder)

        if os.path.isdir(batch_path):
            print(f"Processing batch: {batch_folder}")

            for book_folder in os.listdir(batch_path):
                book_path = os.path.join(batch_path, book_folder)
                images_folder = os.path.join(book_path, "IMAGES")
                excel_file = os.path.join(book_path, "MAIN.xlsx")

                if os.path.isdir(images_folder) and os.path.exists(excel_file):
                    print(f"Processing book: {batch_folder}/{book_folder}")
                    data = load_data(excel_file)

                    try:
                        run_for_book(page, book_folder, data)
                    except Exception as e:
                        print(f"Error processing {batch_folder}/{book_folder}: {e}")
                        failed_books.append(
                            {"Book": f"{batch_folder}/{book_folder}", "Error": str(e)}
                        )
                        # Go back to library page after failure
                        page.goto("https://student.rubiiread.com/library")
                        page.wait_for_timeout(10000)
                else:
                    print(
                        f"Skipping {book_folder}: Required files/folders are missing."
                    )

    if failed_books:
        with open("failed_books.csv", "w", newline="") as csvfile:
            fieldnames = ["Book", "Error"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(failed_books)

    context.close()
    browser.close()


# Run the script with Playwright
with sync_playwright() as playwright:
    run(playwright)

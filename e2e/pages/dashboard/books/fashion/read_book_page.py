from playwright.sync_api import Page
import requests


class BookReadPage:
    def __init__(self, page: Page):
        self.page = page

    def read_book(self):
        self.page.get_by_text("Read", exact=True).click()

    def allow_access(self):
        self.page.wait_for_timeout(10000)
        self.page.get_by_text("Allow Access", exact=True).click()

    def click_microphone(self):
        self.page.locator('img[src="/assets/images/book/mic.png"]').click()

    def get_total_pages(self):
        flipbook_text = (
            self.page.locator("//div[4]/div[1]/div/div[2]/div").text_content().strip()
        )
        return int(flipbook_text.split("/")[1])

    def flip_pages(self, book_name: str, total_pages: int, writer):
        base_url = "https://augie-read.s3.eu-west-2.amazonaws.com/books/"
        book_key = book_name.replace(",", "").replace(
            " ", "_"
        )  # Format book name for URL

        for page_no in range(1, total_pages + 1):
            # Generate the expected image URL for the current page
            image_url = f"{base_url}{book_key}_{page_no}.jpg"

            # Check image accessibility
            try:
                response = requests.head(image_url, timeout=5)  # Timeout in seconds
                image_status = (
                    "Accessible" if response.status_code == 200 else "Not Accessible"
                )
            except requests.RequestException:
                image_status = "Not Accessible"

            # Write to CSV with the image URL and its status
            writer.writerow(
                [
                    book_name,
                    page_no,
                    image_url,
                    image_status,
                ]
            )

            # Flip to the next page
            self.page.wait_for_timeout(5000)
            self.page.locator('img[src="/assets/images/book/left-btn.png"]').click()

            # Ensure API calls are handled
            api_urls = [
                "**/save-audio/",
                "**/update-assignment/**/",
                "**/get-running-record/",
                "**/save-problem-words/**/",
            ]
            for url in api_urls:
                self.page.wait_for_load_state("domcontentloaded")
                self.page.expect_response(
                    lambda response: url in response.url and response.status == 200,
                    timeout=30000,
                )

    def close_book(self):
        self.page.get_by_text("Continue").click()

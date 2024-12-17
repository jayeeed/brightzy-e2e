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
        for page_no in range(1, total_pages + 1):

            with self.page.expect_response("**/books/chapters/**") as response_info:
                response = response_info.value
                data = response.json()

            base_url = "https://augie-read.s3.eu-west-2.amazonaws.com/books/"
            image_url = data["chapters"][0]["image_url"]
            full_url = base_url + image_url

            image_status = "200" if requests.get(full_url).status_code == 200 else "404"

            # Write to CSV with additional index for clarity
            writer(
                [
                    book_name,
                    page_no,
                    full_url,
                    image_status,
                ]
            )

            self.page.wait_for_timeout(5000)
            self.page.wait_for_load_state("domcontentloaded")
            self.page.locator('img[src="/assets/images/book/left-btn.png"]').click()

    def close_book(self):
        self.page.get_by_text("Continue").click()

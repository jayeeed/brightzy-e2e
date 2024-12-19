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
        self.page.wait_for_timeout(5000)
        self.page.locator('img[src="/assets/images/book/mic.png"]').click()
        self.page.reload()
        self.page.wait_for_timeout(5000)
        self.page.locator('img[src="/assets/images/book/mic.png"]').click()

    def get_total_pages(self):
        flipbook_text = (
            self.page.locator("//div[4]/div[1]/div/div[2]/div").text_content().strip()
        )
        return int(flipbook_text.split("/")[1])

    def chapter_url(self):
        with self.page.expect_response("**/books/chapters/**") as response_info:
            response = response_info.value
            data = response.json()
        return data

    def flip_pages(self, book_name: str, total_pages: int, writer):
        data = self.chapter_url()
        base_url = "https://augie-read.s3.eu-west-2.amazonaws.com/books/"

        # Iterate through the chapters from the API response
        for page_data in data["chapters"]:
            page_no = page_data["page"]  # Get the current page number
            image_url = page_data["image_url"]  # Get the image URL for the current page
            full_url = f"{base_url}{image_url}"  # Construct the full image URL

            # Check if the image URL is accessible
            image_status = "200" if requests.get(full_url).status_code == 200 else "404"

            # Write the information to the CSV
            writer.writerow(
                [
                    book_name,
                    page_no,
                    full_url,
                    image_status,
                ]
            )

            # Flip to the next page in the UI if it's not the last page
            if page_no < total_pages + 1:
                self.page.wait_for_timeout(5000)
                self.page.locator('img[src="/assets/images/book/left-btn.png"]').click()

    def asset_accessibility(self):
        self.page.expect_response("click_the_blue_circle_to_start_reading.mp3")
        self.page.expect_response("go-back.png")
        self.page.expect_response("mic.png")

    def close_book(self):
        self.page.get_by_text("Continue").click()

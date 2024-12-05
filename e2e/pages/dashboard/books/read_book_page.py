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

    def flip_pages(self, book_name: str, total_pages: int, writer, sno: int):
        for page_no in range(1, total_pages + 1):
            self.page.wait_for_timeout(5000)
            self.page.wait_for_load_state("domcontentloaded")
            self.page.locator('img[src="/assets/images/book/left-btn.png"]').click()

            # Locate all image-holder elements
            image_elements = self.page.locator(
                "//*[@id='flipbook']/div[2]/div/div"
            ).all()

            for idx, image_element in enumerate(image_elements):
                style_attr = image_element.get_attribute("style")
                if style_attr and "background-image" in style_attr:
                    # Extract image URL
                    start_index = style_attr.find("url(") + 4
                    end_index = style_attr.find(")", start_index)
                    image_url = style_attr[start_index:end_index].strip('"').strip("'")
                    full_url = image_url

                    # Check image accessibility
                    response = requests.head(full_url, timeout=5000)
                    image_status = (
                        "Accessible"
                        if response.status_code == 200
                        else "Not Accessible"
                    )
                else:
                    full_url = None
                    image_status = "No Image Found"

            # Write to CSV with additional index for clarity
            writer.writerow(
                [
                    sno,
                    book_name,
                    page_no,
                    full_url,
                    image_status,
                ]
            )

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

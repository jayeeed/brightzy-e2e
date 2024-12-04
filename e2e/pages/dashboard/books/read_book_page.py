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

    def image_accessibility(self):
        # TODO: use api to check image accessibility
        # Locate the divs with the background-image style (class name contains 'image-holder')
        elements_with_background = self.page.locator(
            "div[class*='image-holder'][style*='background-image']"
        )
        count = elements_with_background.count()
        image_data = []

        for i in range(count):
            # Extract the background-image URL
            style = elements_with_background.nth(i).evaluate(
                "el => el.style.backgroundImage"
            )
            if style and "url(" in style:
                # Clean up the URL to remove extra quotes or characters
                image_url = (
                    style.split("url(")[1]
                    .split(")")[0]
                    .strip('"')
                    .strip("'")
                    .replace("&quot;", "")
                )

                # Check if the image URL is accessible
                status_code = self.check_image_status(image_url)

                # Append image URL and status code to image_data
                image_data.append((image_url, status_code))

        return image_data  # Return list of tuples (image_url, status_code)

    def check_image_status(self, image_url: str):
        try:
            response = requests.get(image_url, timeout=1000)
            return response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {image_url}: {e}")
            return None

    def flip_pages(self, book_name: str, total_pages: int, writer, sno: int):
        for page_no in range(1, total_pages + 1):
            self.page.wait_for_timeout(5000)
            self.page.locator('img[src="/assets/images/book/left-btn.png"]').click()

            image_data = self.image_accessibility()

            page_image_url = image_data[0][0] if image_data else "No Image URL"
            page_status_code = image_data[0][1] if image_data else "No Status Code"

            writer.writerow(
                [sno, book_name, total_pages, page_no, page_image_url, page_status_code]
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

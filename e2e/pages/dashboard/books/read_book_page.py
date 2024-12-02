from playwright.sync_api import Page


class BookReadPage:
    def __init__(self, page1: Page):
        self.page = page1

    def read_book(self):
        self.page.get_by_text("Read book").click()

    def allow_access(self):
        self.page.get_by_text("Allow Access", exact=True).click()

    def click_microphone(self):
        self.page.locator('img[src="/assets/images/book/mic.png"]').click()

    def get_total_pages(self):
        flipbook_text = (
            self.page.locator("//div[4]/div[1]/div/div[2]/div").text_content().strip()
        )
        return int(flipbook_text.split("/")[1])

    def flip_pages(self, total_pages: int):
        for _ in range(total_pages):
            self.page.locator('img[src="/assets/images/book/left-btn.png"]').click()

    def close_book(self):
        self.page.get_by_text("Continue").click()
        self.page.locator('img[src="/assets/images/arrowLeftz.png"]').click()
        

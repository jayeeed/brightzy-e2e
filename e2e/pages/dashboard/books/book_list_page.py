from playwright.sync_api import Page


class BookListPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_books(self, clicks=3):
        for _ in range(clicks):
            self.page.locator(".right > .arrowDesign").first.click()

    def select_first_book(self):
        self.page.locator(".viewMoreBookImg").first.click()

    def get_books(self):
        return self.page.locator("//app-book/div/div[1]/img")

    def get_book_name(self):
        return self.page.text_content("//h2")

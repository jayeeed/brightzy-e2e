from playwright.sync_api import Page


class BookListPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_books(self):
        self.page.goto(
            "https://student-staging.brightzy.com/library/book-list/4?languageCode=en-US"
        )

    def list_page(self, page_number: int):
        self.page.get_by_text(f"page {page_number}").click()

    def get_books(self):
        return self.page.locator("//app-book/div/div[1]/img")

    def get_book_name(self):
        return self.page.text_content("//app-bookactionselection/div/div/div[2]/p")

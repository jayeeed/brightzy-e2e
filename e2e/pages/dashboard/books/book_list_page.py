from playwright.sync_api import Page


class BookListPage:
    def __init__(self, page: Page):
        self.page = page

    # def navigate_books(self, clicks=1):
    #     for _ in range(clicks):
    #         self.page.locator(
    #             "//div[1]/div/app-single-category-book-list/div[2]/div[2]/img"
    #         ).click()
    #         self.page.locator("//div[2]/div[11]/img").click()
    #         self.page.wait_for_timeout(3000)

    def navigate_books(self):
        self.page.goto(
            "https://student-staging.brightzy.com/library/book-list/12?languageCode=en-US"
        )

    def get_books(self):
        return self.page.locator("//app-book/div/div[1]/img")

    def get_book_name(self):
        return self.page.text_content("//app-bookactionselection/div/div/div[2]/p")

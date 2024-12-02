from playwright.sync_api import Page


class StudentDashboardPage:
    def __init__(self, page: Page):
        self.page = page

    def close_banner(self):
        self.page.locator("img[src='/assets/images/Cross_button.webp']").click()

    def goto_learning_journey(self):
        self.page.get_by_text("LEARNING JOURNEY").click()

    def goto_reading_activities(self):
        self.page.get_by_text("READING ACTIVITIES").click()

    def goto_books(self):
        self.page.get_by_text("BOOKS").click()

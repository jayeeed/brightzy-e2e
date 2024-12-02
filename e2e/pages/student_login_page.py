from playwright.sync_api import Page


class StudentLoginPage:
    def __init__(self, page: Page):
        self.page = page

    def select_student(self):
        with self.page.expect_popup() as page1_info:
            self.page.locator("//tr[1]/td[4]/button/span[1]").click()
        page1 = page1_info.value
        self.page.close()
        return page1

from playwright.sync_api import Page


class StudentLoginPage:
    def __init__(self, page: Page):
        self.page = page

    def select_student(self):
        with self.page.expect_popup() as page1_info:
            self.page.locator("//tr[2]/td[4]/button/span[1]").click()
        page1 = page1_info.value
        self.page.close()
        return page1

    def direct_login(self):
        self.page.goto("https://student-staging.brightzy.com/login")
        self.page.wait_for_timeout(3000)
        self.page.get_by_text("Sign In").click()
        self.page.get_by_label("Sign In").get_by_role("textbox").click()
        self.page.get_by_role("textbox").fill("44585537")
        self.page.get_by_role("button", name="Sign In").click()

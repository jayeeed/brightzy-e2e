from playwright.sync_api import Page


class ParentLoginPage:
    def __init__(self, page: Page):
        self.page = page

    def goto_login_page(self):
        self.page.goto("https://parent-staging.brightzy.com/login")

    def login(self, email: str, password: str):
        self.page.get_by_placeholder("e.g. email@domain.com").fill(email)
        self.page.get_by_placeholder("Enter your password").fill(password)
        self.page.get_by_role("button", name="Log In").click()

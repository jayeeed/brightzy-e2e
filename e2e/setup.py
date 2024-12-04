from playwright.sync_api import Playwright


class Setup:
    def __init__(self):
        self.browser = None
        self.context = None

    def setup_browser(self, playwright: Playwright):
        self.browser = playwright.chromium.launch(
            headless=False,
            slow_mo=500,
            args=[
                "--start-maximized",
                "--mute-audio",
                "--use-fake-ui-for-media-stream",
            ],
        )
        self.context = self.browser.new_context()
        self.context.set_default_timeout(60000)
        self.context.grant_permissions(permissions=["microphone"])
        return self.browser, self.context

    def close_browser(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()

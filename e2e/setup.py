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
                # "--start-maximized",
                "--mute-audio",
                "--use-fake-ui-for-media-stream",
            ],
        )
        self.context = self.browser.new_context(viewport={"width": 1280, "height": 600})
        self.context.set_default_timeout(1200000)
        self.context.grant_permissions(permissions=["microphone"])

        # Start tracing
        self.context.tracing.start(screenshots=True, snapshots=True, sources=True)
        return self.browser, self.context

    def close_browser(self, trace_path="trace.zip"):
        if self.context:
            # Stop tracing and export it into a zip archive
            self.context.tracing.stop(path=trace_path)
            self.context.close()
        if self.browser:
            self.browser.close()

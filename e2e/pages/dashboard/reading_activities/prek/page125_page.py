from playwright.sync_api import Page


class page125Page:
    def __init__(self, page: Page):
        self.page = page

    def goto_prek_alphabet_sound_5(self):
        self.page.get_by_text("Pre-k").click()
        self.page.get_by_text("Alphabet Letters", exact=True).click()

    def complete_activity(self):
        for div_index in range(1, 11):
            self.page.locator(
                f"//app-game-category-list/div/div[2]/div[{div_index}]/div/div//button/p[contains(text(), 'Start') or contains(text(), 'Continue')]"
            ).click()

            with self.page.expect_response("**/word/game/level/**") as response_info:
                response = response_info.value
                category_scene = response.json()["data"]["category_scene"]

            if category_scene in ["page1", "page2"]:
                self.first(category_scene)
            elif category_scene == "page3":
                self.second()
            elif category_scene in ["page4", "page5"]:
                self.third(category_scene)

            self.finish_activity()

    def first(self, category_scene):
        if self.page.get_by_text("Allow Access", exact=True).is_visible():
            self.page.wait_for_timeout(10000)
            self.page.get_by_text("Allow Access", exact=True).click()

        loop_count = 2 if category_scene == "page1" else 1

        self.perform_button_clicks(loop_count)

    def second(self):
        # TODO: fix - not clicking button
        if self.page.locator(
            "img[src='/assets/images/sound icon_with_question.png']"
        ).is_visible():
            self.page.wait_for_timeout(10000)
            self.page.locator(
                "img[src='/assets/images/sound icon_with_question.png']"
            ).click()
            self.page.locator(
                "img[src='/assets/images/sound icon_with_question.png']"
            ).click()
            self.page.locator(
                "img[src='/assets/images/sound icon_with_question.png']"
            ).click()
            self.page.wait_for_timeout(10000)

    def third(self, category_scene):
        if self.page.get_by_text("Allow Access", exact=True).is_visible():
            self.page.wait_for_timeout(10000)
            self.page.get_by_text("Allow Access", exact=True).click()

        loop_count = 4 if category_scene == "page4" else 2

        self.perform_button_clicks(loop_count)

    def perform_button_clicks(self, loop_count):
        for _ in range(loop_count):
            self.page.wait_for_timeout(10000)
            self.page.wait_for_selector("img[src='/assets/images/blueBtn.png']").click()
            self.page.wait_for_timeout(5000)
            self.page.wait_for_selector("img[src='/assets/images/redBtn.png']").click()

    def finish_activity(self):
        self.page.get_by_alt_text("CONTINUE").click()

from playwright.sync_api import Page


class lowercaseAlphabetPage:
    def __init__(self, page: Page):
        self.page = page

    def goto_prek_apb_lca_10(self):
        self.page.get_by_text("Pre-k").click()
        self.page.get_by_text("Alphabet", exact=True).click()

    def start_activity(self):
        self.page.get_by_role("button", name="Continue").click()

    def complete_activity(self):
        with self.page.expect_response("**/966/") as response_info:
            response = response_info.value
            data = response.json()

        correct_option = next(
            (
                opt["option"]
                for opt in data["data"]["game_data"]["options"]
                if opt["is_correct"]
            ),
            None,
        )

        if correct_option:
            self.page.get_by_text(correct_option, exact=True).click(force=True)

    def finish_activity(self):
        self.page.get_by_alt_text("CONTINUE").click()

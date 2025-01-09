import json
from e2e.setup import Setup
from e2e.pages.parent_login_page import ParentLoginPage
from e2e.pages.student_login_page import StudentLoginPage
from e2e.pages.dashboard.student_dashboard_page import StudentDashboardPage
from e2e.pages.dashboard.reading_activities.prek.lowercaseAlphabet_page import (
    lowercaseAlphabetPage,
)

from playwright.sync_api import sync_playwright
import pytest


# @pytest.mark.skip(reason="Skipping for now")
def test_lowercaseAlphabet():
    with sync_playwright() as playwright:
        setup = Setup()
        browser, context = setup.setup_browser(playwright)
        page = context.new_page()

        # Login
        login_page = ParentLoginPage(page)
        login_page.goto_login_page()

        with open("e2e/config/login_data.json") as json_file:
            config = json.load(json_file)["user_credentials"]
        login_page.login(config["email"], config["password"])

        # Select Student
        dashboard_page = StudentLoginPage(page)
        student_page = dashboard_page.select_student()

        # Select Reading Activities
        student_dashboard_page = StudentDashboardPage(student_page)
        student_dashboard_page.close_banner()
        student_dashboard_page.goto_reading_activities()

        # Perform Activity
        activity_page = lowercaseAlphabetPage(student_page)
        activity_page.goto_prek_apb_lca_10()
        activity_page.start_activity()

        for _ in range(10):  # Loop through questions
            activity_page.complete_activity()

        activity_page.finish_activity()

        # Teardown - Close browser
        setup.close_browser()

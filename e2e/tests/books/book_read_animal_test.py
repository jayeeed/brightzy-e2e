import csv
import json
from e2e.setup import Setup
from e2e.pages.parent_login_page import ParentLoginPage
from e2e.pages.student_login_page import StudentLoginPage
from e2e.pages.dashboard.student_dashboard_page import StudentDashboardPage
from e2e.pages.dashboard.books.book_list_page import BookListPage
from e2e.pages.dashboard.books.read_book_page import BookReadPage

from playwright.sync_api import sync_playwright


def test_book_read_animal():
    with sync_playwright() as playwright:
        setup = Setup()
        browser, context = setup.setup_browser(playwright)
        page = context.new_page()

        # # Login
        # login_page = ParentLoginPage(page)
        # login_page.goto_login_page()

        # with open("e2e/config/login_data.json") as json_file:
        #     config = json.load(json_file)["user_credentials"]
        # login_page.login(config["email"], config["password"])

        # Select Student
        dashboard_page = StudentLoginPage(page)
        # student_page = dashboard_page.select_student()
        dashboard_page.direct_login()

        # Select Reading Activities
        student_dashboard_page = StudentDashboardPage(page)
        student_dashboard_page.close_banner()
        student_dashboard_page.goto_books()

        # Prepare CSV file
        with open("books_read_animal.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "Book Name",
                    "Page No",
                    "Image URL",
                    "Status Code",
                ]
            )

            # Navigate and read books
            book_list_page = BookListPage(page)
            book_list_page.navigate_books()
            books = book_list_page.get_books()
            book_count = books.count()

            for i in range(book_count):
                books.nth(i).click()
                book_name = book_list_page.get_book_name()

                read_book_page = BookReadPage(page)
                read_book_page.read_book()

                if i == 0:
                    read_book_page.allow_access()

                # read_book_page.asset_accessibility()
                read_book_page.click_microphone()

                total_pages = read_book_page.get_total_pages()

                # Flip pages and log dynamically, including image URL and status code
                read_book_page.flip_pages(book_name, total_pages, writer)

                read_book_page.close_book()

        # Teardown - Close browser
        setup.close_browser()

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def login_action(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def assert_error_message(self, text: str) -> None:
        expect(self.error_message).to_have_text(text)

    def login(self, username: str, password: str) -> "InventoryPage":
        self.login_action(username, password)
        return InventoryPage(self.page)

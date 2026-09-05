import pytest

from config.settings import credentials


@pytest.mark.regression
class TestLoginPage():
    @pytest.mark.smoke
    def test_login(self, login_page) -> None:
        login_page.navigate()
        inventory_page = login_page.login(credentials.standard_user, credentials.password)
        inventory_page.assert_product_sort_container_to_be_visible()

    @pytest.mark.parametrize("username,password,error", [
        (
                credentials.incorrect_username_or_password,
                credentials.incorrect_username_or_password,
                "Epic sadface: Username and password do not match any user in this service"
        ),
        (
                credentials.locked_out_user,
                credentials.password,
                "Epic sadface: Sorry, this user has been locked out."
        ),
    ])
    def test_login_error(self, login_page, username, password, error) -> None:
        login_page.navigate()
        login_page.login_action(username, password)
        login_page.assert_error_message(error)

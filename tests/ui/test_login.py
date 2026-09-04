import pytest

from config.settings import credentials


@pytest.mark.regression
class TestLoginPage():
    @pytest.mark.smoke
    def test_login(self, login_page) -> None:
        login_page.navigate()
        inventory_page = login_page.login(credentials.standard_user, credentials.password)
        inventory_page.wait_for_product_sort_container()

    @pytest.mark.parametrize("username,password", [
        (credentials.incorrect_username_or_password, credentials.incorrect_username_or_password),
        (credentials.locked_out_user, credentials.password)
    ])
    def test_login_error(self, login_page, username, password) -> None:
        login_page.navigate()
        login_page.login_action(username, password)
        login_page.assert_error_message(
            'Epic sadface: Sorry, this user has been locked out.'
            if username == credentials.locked_out_user
            else 'Epic sadface: Username and password do not match any user in this service')

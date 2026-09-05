import pytest

from config.settings import credentials, product_items


@pytest.mark.regression
class TestCartPage():
    @pytest.mark.smoke
    def test_check_cart(self, login_page) -> None:
        login_page.navigate()
        inventory_page = login_page.login(credentials.standard_user, credentials.password)
        inventory_page.add_to_cart(product_items["backpack"])
        inventory_page.add_to_cart(product_items["onesie"])

        cart_page = inventory_page.open_cart()
        cart_page.assert_checkout_button_to_be_visible()
        cart_page.assert_cart_items_amount(2)
        cart_page.assert_cart_item(product_items["backpack"])
        cart_page.assert_cart_item(product_items["onesie"])
import pytest

from config.settings import credentials, product_items


@pytest.mark.regression
class TestCartPage():
    def test_add_item_to_cart(self, login_page) -> None:
        login_page.navigate()
        inventory_page = login_page.login(credentials.standard_user, credentials.password)
        inventory_page.add_to_cart(product_items["backpack"])
        inventory_page.assert_cart_badge_count(1)
        inventory_page.add_to_cart(product_items["onesie"])
        inventory_page.assert_cart_badge_count(2)
        inventory_page.add_to_cart(product_items["fleece_jacket"])
        inventory_page.assert_cart_badge_count(3)
        inventory_page.remove_from_cart(product_items["fleece_jacket"])
        inventory_page.assert_cart_badge_count(2)
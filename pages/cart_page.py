from playwright.sync_api import Page, expect

from config.settings import ProductItem
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.checkout_button = page.get_by_test_id("checkout")
        self.inventory_item = page.get_by_test_id("inventory-item")

    def wait_for_checkout_button(self) -> None:
        self.checkout_button.wait_for(timeout=2000)

    def assert_cart_items_amount(self, count: int) -> None:
        expect(self.inventory_item).to_have_count(count)

    def inventory_item_name(self, item_id: str):
        return self.page.get_by_test_id(item_id).get_by_test_id("inventory-item-name")

    def inventory_item_price(self, item_id: str):
        item = self.page.get_by_test_id("inventory-item").filter(
            has=self.page.get_by_test_id(item_id)
        )
        return item.get_by_test_id("inventory-item-price")

    def assert_cart_item(self, product: ProductItem) -> None:
        expect(self.inventory_item_name(product.item_id)).to_have_text(product.name)
        expect(self.inventory_item_price(product.item_id)).to_have_text(product.price)

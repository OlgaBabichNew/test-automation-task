from playwright.sync_api import Page, expect

from config.settings import ProductItem
from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.product_sort = page.get_by_test_id("product-sort-container")
        self.shopping_cart_icon = page.get_by_test_id("shopping-cart-link")
        self.shopping_cart_badge = page.get_by_test_id("shopping-cart-badge")

    def wait_for_product_sort_container(self) -> None:
        self.product_sort.wait_for(timeout=2000)

    def add_button(self, attribute: str):
        return self.page.get_by_test_id(f"add-to-cart-{attribute}")

    def remove_button(self, attribute: str):
        return self.page.get_by_test_id(f"remove-{attribute}")

    def add_to_cart(self, product: ProductItem) -> None:
        self.add_button(product.attribute).click()

    def remove_from_cart(self, product: ProductItem) -> None:
        self.remove_button(product.attribute).click()

    def assert_cart_badge_count(self, expected: int) -> None:
        expect(self.shopping_cart_badge).to_have_text(str(expected))

    def open_cart(self) -> "CartPage":
        self.shopping_cart_icon.click()
        return CartPage(self.page)
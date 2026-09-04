from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url: str = "https://www.example.com"
    browser: str = "chromium"  # chromium | firefox | webkit
    headless: bool = True
    test_id_attribute: str = "data-test"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


class Credentials(BaseSettings):
    # Standard user — used for positive login and cart tests.
    standard_user: str = "user1"

    # Locked-out user — used for negative login tests.
    locked_out_user: str = "user2"

    # Incorrect user and password — used for negative login tests.
    incorrect_username_or_password: str = "123"

    # Shared password for all demo accounts on saucedemo.com.
    password: str = "Passw@rd"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


credentials = Credentials()


class ProductItem:
    def __init__(self, name: str, item_id: str, attribute: str, price: str):
        self.name = name
        self.item_id = item_id
        self.attribute = attribute
        self.price = price


product_items = {
    "backpack": ProductItem("Sauce Labs Backpack", "item-4-title-link", "sauce-labs-backpack", "$29.99"),
    "onesie": ProductItem("Sauce Labs Onesie", "item-2-title-link", "sauce-labs-onesie", "$7.99"),
    "fleece_jacket": ProductItem("Sauce Labs Fleece Jacket", "item-5-title-link", "sauce-labs-fleece-jacket", "$49.99"),
}

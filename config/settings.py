from pydantic import BaseModel, ConfigDict
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


class ProductItem(BaseModel):
    name: str
    item_id: str
    attribute: str
    price: str

    model_config = ConfigDict(frozen=True)


product_items = {
    "backpack": ProductItem(name="Sauce Labs Backpack", item_id="item-4-title-link", attribute="sauce-labs-backpack", price="$29.99"),
    "onesie": ProductItem(name="Sauce Labs Onesie", item_id="item-2-title-link", attribute="sauce-labs-onesie", price="$7.99"),
    "fleece_jacket": ProductItem(name="Sauce Labs Fleece Jacket", item_id="item-5-title-link", attribute="sauce-labs-fleece-jacket", price="$49.99"),
}

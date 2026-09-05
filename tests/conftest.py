import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.login_page import LoginPage

# Configure the test-id attribute for Playwright's get_by_test_id() locator
@pytest.fixture(scope="session", autouse=True)
def set_test_id_attribute(playwright) -> None:
    playwright.selectors.set_test_id_attribute(settings.test_id_attribute)


# Override pytest-playwright built-ins — picked up automatically, no explicit call needed
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": settings.base_url,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "headless": settings.headless,
    }


@pytest.fixture(scope="session")
def browser_name() -> str:
    return settings.browser


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

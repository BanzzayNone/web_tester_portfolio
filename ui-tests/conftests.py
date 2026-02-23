import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    new_page = context.new_page()
    yield new_page
    context.close()
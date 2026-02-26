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

#  Фикстура с тестовыми данными (function scope — изоляция тестов)
@pytest.fixture
def credentials():
    return {
        "valid": {"username": "Admin", "password": "admin123"},
        "invalid_username": {"username": "WrongUser", "password": "admin123"},
        "login_button": "button[type='submit']",
        "error_message": ".oxd-alert-content-text",
        "dashboard_heading": ".oxd-topbar-header-breadcrumb h6"  # после успешного входа
    }

#  Фикстура с селекторами (легко поддерживать при изменении вёрстки)
@pytest.fixture
def login_selectors():
    return {
        "username_input": "input[name='username']",
        "password_input": "input[name='password']",
        "login_button": "button[type='submit']",
        "error_message": ".oxd-alert-content-text",
        "dashboard_heading": ".oxd-topbar-header-breadcrumb h6"  # после успешного входа
    }
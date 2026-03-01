import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    """ Открытие браузера, один на все тесты из-за параметра - session """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
def page(browser):
    """ Открываем страницу на каждый тест, контекст у всех один """
    context = browser.new_context()
    new_page = context.new_page()
    yield new_page
    context.close()

@pytest.fixture
def credentials():
    """ Фикстура с тестовыми данными (function scope — изоляция тестов) """
    return {
        "valid": {"username": "Admin", "password": "admin123"},
        "invalid_username": {"username": "WrongUser", "password": "admin123"},
        "login_button": "button[type='submit']",
        "error_message": ".oxd-alert-content-text",
        "dashboard_heading": ".oxd-topbar-header-breadcrumb h6"  # после успешного входа
    }

@pytest.fixture
def login_selectors():
    """ Фикстура с селекторами (легко поддерживать при изменении вёрстки) """
    return {
        "username_input": "input[name='username']",
        "password_input": "input[name='password']",
        "login_button": "button[type='submit']",
        "error_message": ".oxd-alert-content-text",
    }
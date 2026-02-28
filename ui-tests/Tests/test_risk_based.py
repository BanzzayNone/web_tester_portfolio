import pytest
from playwright.sync_api import Page, expect

def test_login_valid_credentials(page: Page, credentials, login_selectors, base_url):
    """Успешная авторизация с валидными данными"""
    page.goto("BASE_URL")
    
    # Заполняем форму
    page.locator(login_selectors["username_input"]).fill(credentials["valid"]["username"])
    page.locator(login_selectors["password_input"]).fill(credentials["valid"]["password"])
    page.locator(login_selectors["login_button"]).click()
    
    # Проверяем переход на дашборд (бизнес-логика: успешный вход = видим заголовок)
    expect(page.locator(login_selectors["dashboard_heading"])).to_be_visible(timeout=10000)
    assert "Dashboard" in page.title() or page.url.endswith("/dashboard")


def test_login_invalid_username(page: Page, credentials, login_selectors):
    """Авторизация с неверным username — ошибка валидации"""
    page.goto("BASE_URL")
    
    page.locator(login_selectors["username_input"]).fill(credentials["invalid_username"]["username"])
    page.locator(login_selectors["password_input"]).fill(credentials["invalid_username"]["password"])
    page.locator(login_selectors["login_button"]).click()
    
    # Проверяем сообщение об ошибке (бизнес-логика: система не пускает с неверными данными)
    expect(page.locator(login_selectors["error_message"])).to_contain_text(
        "Invalid credentials", timeout=10000
    )
    # Убеждаемся, что остались на странице логина
    assert "auth/login" in page.url


def test_login_empty_fields(page: Page, credentials, login_selectors):
    """Попытка входа с пустыми полями — валидация на фронтенде"""
    page.goto("BASE_URL")
    
    # Пытаемся нажать Login без заполнения полей
    page.locator(login_selectors["login_button"]).click()
    
    # Проверяем, что поля подсветились как обязательные (бизнес-правило: поля required)
    expect(page.locator(login_selectors["username_input"])).to_have_class("oxd-input oxd-input--active")
    # Или проверяем наличие атрибута required
    assert page.locator(login_selectors["username_input"]).get_attribute("required") is not None


def test_page_elements_present(page: Page, login_selectors):
    """Критические UI-элементы страницы авторизации присутствуют"""
    page.goto("BASE_URL")
    
    # Проверяем наличие всех ключевых элементов (бизнес-логика: страница должна быть готова к использованию)
    expect(page.locator(login_selectors["username_input"])).to_be_visible()
    expect(page.locator(login_selectors["password_input"])).to_be_visible()
    expect(page.locator(login_selectors["login_button"])).to_be_visible()
    expect(page.locator(login_selectors["login_button"])).to_have_text("Login")
    
    # Ссылка восстановления пароля — часть бизнес-процесса
    expect(page.get_by_text("Forgot your password?")).to_be_visible()
    
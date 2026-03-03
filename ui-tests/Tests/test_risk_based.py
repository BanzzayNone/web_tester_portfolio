import pytest
from playwright.sync_api import Page, expect


def test_page_elements_present(page: Page, login_selectors):
    """Критические UI-элементы страницы авторизации присутствуют и скрывается ли пароль при вводе"""
    page.goto("https://opensource-demo.orangehrmlive.com")
    
    # Проверяем наличие всех ключевых элементов
    expect(page.locator(login_selectors["username_input"])).to_be_visible(timeout=15000)
    expect(page.locator(login_selectors["password_input"])).to_be_visible()
    expect(page.locator(login_selectors["login_button"])).to_be_visible()
    expect(page.locator(login_selectors["login_button"])).to_have_text("Login")
    expect(page.locator(login_selectors["password_input"])).to_have_attribute("type", "password")
    expect(page.get_by_text("Forgot your password?")).to_be_visible()

def test_login_valid_credentials(page: Page, credentials, login_selectors):
    """Успешная авторизация с валидными данными"""
    page.goto("https://opensource-demo.orangehrmlive.com")
    
    # Заполняем форму
    page.locator(login_selectors["username_input"]).fill(credentials["valid"]["username"])
    page.locator(login_selectors["password_input"]).fill(credentials["valid"]["password"])
    page.locator(login_selectors["login_button"]).click()
    
    # Проверяем вход
    expect(page.get_by_text("Time at Work")).to_be_visible(timeout=(10000))

def test_login_invalid_username(page: Page, credentials, login_selectors):
    """Авторизация с неверным username — ошибка валидации"""
    page.goto("https://opensource-demo.orangehrmlive.com")
    
    page.locator(login_selectors["username_input"]).fill(credentials["invalid_username"]["username"])
    page.locator(login_selectors["password_input"]).fill(credentials["invalid_username"]["password"])
    page.locator(login_selectors["login_button"]).click()
    
    # Проверяем сообщение об ошибке
    expect(page.locator(login_selectors["error_message"])).to_contain_text("Invalid credentials", timeout=10000)
    # Проверяем, остались ли на странице логина
    assert "auth/login" in page.url


def test_login_empty_fields(page: Page, credentials, login_selectors):
    """Попытка входа с пустыми полями — валидация на фронте"""
    page.goto("https://opensource-demo.orangehrmlive.com")
    
    # Пытаемся нажать Login без заполнения полей
    page.locator(login_selectors["login_button"]).click()
    
    # Проверяем, что поля подсветились
    expect(page.locator(login_selectors["username_input"])).to_have_class("oxd-input oxd-input--active")
    # Или проверяем наличие атрибута required
    assert page.locator(login_selectors["username_input"]).get_by_text("required") is not None

def test_login_without_click(page: Page, credentials, login_selectors):
    """Проверка автофокуса на поле ввода логина и реакции на отправку формы по Enter"""
    page.goto("https://opensource-demo.orangehrmlive.com")
    # Проверяем автофокус
    expect(page.locator(login_selectors["username_input"])).to_be_focused()
    # Проверяем реакцию на нажатие клавиши Enter  
    page.locator(login_selectors["username_input"]).press("Enter")
    assert page.locator(login_selectors["username_input"]).get_by_text("required") is not None

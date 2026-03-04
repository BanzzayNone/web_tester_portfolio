import pytest
from playwright.sync_api import Page, expect


def test_page_elements_present(page: Page, login_selectors):
    """Критические UI-элементы страницы авторизации присутствуют и скрывается ли пароль при вводе"""
    page.goto("https://opensource-demo.orangehrmlive.com")
    
    # Проверяем наличие всех ключевых элементов
    expect(page.locator(login_selectors["username_input"])).to_be_visible(timeout=15000) # Таймаут для загрузки, на случай если затянется
    expect(page.locator(login_selectors["password_input"])).to_be_visible()
    expect(page.locator(login_selectors["login_button"])).to_be_visible()
    expect(page.locator(login_selectors["login_button"])).to_have_text("Login")
    expect(page.locator(login_selectors["password_input"])).to_have_attribute("type", "password")
    expect(page.get_by_text("Forgot your password?")).to_be_visible()


def test_login_valid_credentials(page: Page, credentials, login_selectors):
    """Успешная авторизация с валидными данными + проверка запроса после"""
    page.goto("https://opensource-demo.orangehrmlive.com")
    
    # Заполняем форму
    page.locator(login_selectors["username_input"]).fill(credentials["valid"]["username"])
    page.locator(login_selectors["password_input"]).fill(credentials["valid"]["password"])
    # Ловим запросы  
    with page.expect_request("**/auth/validate") as request_info:
        page.locator(login_selectors["login_button"]).click()
    request = request_info.value
    response = request.response()
    assert request.method == "POST"
    assert response.status == 302 # будет 302, после успешного входа нас перенаправляют
    # Теперь проверим куки на наличие нужной
    cookies = page.context.cookies()
    auth_cookie = next((c for c in cookies if c.get("name") == "orangehrm"), None)
    assert len(auth_cookie["value"]) > 0, "Значение куки пустое"
    
    # Проверим нет ли пароля в URL
    assert "password" not in request.url.lower() 

    # Проверяем успешен ли вход
    expect(page.get_by_text("Time at Work")).to_be_visible()

def test_login_invalid_username(page: Page, credentials, login_selectors):
    """Авторизация с неверным username — ошибка валидации"""
    page.goto("https://opensource-demo.orangehrmlive.com")

    # Заполняем форму
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
    page.goto("https://opensource-demo.orangehrmlive.com", timeout=50000)  # Таймаут для загрузки, на случай если затянется - при хорошем интернете удалить
    # Проверяем автофокус
    expect(page.locator(login_selectors["username_input"])).to_be_focused(timeout=15000) # Таймаут для загрузки, на случай если затянется - при хорошем интернете удалить
    # Проверяем реакцию на нажатие клавиши Enter  
    page.locator(login_selectors["username_input"]).press("Enter")
    assert page.locator(login_selectors["username_input"]).get_by_text("required") is not None
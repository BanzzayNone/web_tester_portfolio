# Стандартные CSS-селекторы для страницы логина
SELECTORS = {
    "username_field": "input[name='username']",  # Поле ввода логина
    "password_field": "input[name='password']",  # Поле ввода пароля
    "login_button": "button[type='submit']",  # Кнопка входа
    "remember_me": "input[type='checkbox']",  # Чекбокс "Remember me"
    "error_message": ".oxd-alert-content-text",  # Сообщение об ошибке
    "dashboard_menu": ".oxd-topbar-header-breadcrumb",  # Элемент, который появляется после успешного входа
    "pim_menu": "a[href*='pim']",  # Пункт меню PIM
    "add_employee_btn": ".oxd-button[href*='addEmployee']",  # Кнопка "Добавить сотрудника"
}
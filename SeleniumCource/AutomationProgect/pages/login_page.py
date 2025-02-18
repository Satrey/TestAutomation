# from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.base_class import Base


class LoginPage(Base):
    """Класс для аутентификации пользователя в интернет магазине"""

    def __init__(self, driver):
        super.__init__(driver)

    # URL тестируемой страницы
    base_url = "https://www.saucedemo.com/"

    # Локаторы спользуемые на странице
    login = "user_name"
    password = "password"
    login_button = "login_button"

    # Геттеры
    def get_input_login(self):
        return WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, self.login))
        )

    def get_input_password(self):
        return WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, self.password))
        )

    def get_login_button(self):
        return WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, self.login_button))
        )

    # Действия
    def input_user_name(self, user_name):
        self.get_input_login().send_keys(user_name)
        print("Ввод имени пользователя в поле Login")

    def input_password(self, password):
        self.get_input_password().send_keys(password)

    def click_login_button(self):
        self.get_login_button().click()

    # Методы
    def autentification(self):
        self.driver.get(self.base_url)
        self.driver.maximize_window()

        self.input_user_name("standard_user")
        self.input_password("secret_sauce")
        self.click_login_button()

import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Учетные данные для входа в интернет магазиин
base_url = "https://www.saucedemo.com/"
login_list = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
]
login = "standard_user"
pwd = "secret_sauce"

# Параметры и опции драйвера
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_experimental_option("detach", True)


class TestAuthPage:
    """
    Класс проверки сценариев аутентификации пользователя в интернет магазине
    """

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    # Метод аутентификации пользователя на сайте магазина
    # Поиск и заполнение полей формы аутентификации
    def login_market(self, login, password):
        wait = WebDriverWait(self.driver, 20)
        # Заполняем поле логин
        field_login = wait.until(EC.element_to_be_clickable((By.ID, "user-name")))
        field_login.send_keys(login)

        # Заполняем поле пароль
        field_password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        field_password.send_keys(password)

        # Нажимаем кнопку входа
        button_login = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        button_login.click()

    # Проверка входа в магазин по логотипу и URL под разными учётками
    def check_auth(self, login):
        wait = WebDriverWait(self.driver, 20)
        match login:
            case "standard_user":
                # Проверка входа в магазин по URL
                assert (
                    self.driver.current_url
                    == "https://www.saucedemo.com/inventory.html"
                ), "Неудача!!! Переход на главную страницу магазина не осуществлен!"
                print(
                    f"Успешно!!! Переход на главную страницу выполнен по адресу {self.driver.current_url}!"
                )

                logo_text = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//span[@class="title"]'))
                )
                assert logo_text.text == "Products", (
                    "Неудача!!! Переход на главную страницу магазина не осуществлен!"
                )
                print("Успешно!!! Переход на главную страницу выполнен!")

            case "locked_out_user":
                # Проверка входа в магазин по URL
                assert self.driver.current_url == "https://www.saucedemo.com/", (
                    "Неудача!!! Выполнен переход на другую страницу!"
                )
                print(
                    f"Успешно!!! Переход на главную страницу заблокирован {self.driver.current_url}!"
                )

                # Проверка присутствия сообщения о блокировке
                alert_box = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//h3[@ data-test="error"]',
                        )
                    )
                )
                assert (
                    alert_box.text
                    == "Epic sadface: Sorry, this user has been locked out."
                ), "Неудача!!! Переход на главную страницу магазина не осуществлен!"
                print("Успешно!!! Сообщение о блокировке пользователя присутствует!")

            case "problem_user":
                pass
            case "performance_glitch_user":
                pass
            case "error_user":
                pass
            case "visual_user":
                pass

    # Очистка формы аутентификации пользователя
    def clear_auth_form(self):
        wait = WebDriverWait(self.driver, 20)
        # Очищаем поле логин
        field_login = wait.until(EC.element_to_be_clickable((By.ID, "user-name")))
        field_login.send_keys(Keys.CONTROL + "a")
        field_login.send_keys(Keys.BACKSPACE)

        # Очищаем поле пароль
        field_password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        field_password.send_keys(Keys.CONTROL + "a")
        field_password.send_keys(Keys.BACKSPACE)

    # Выход пользователя из магазина
    def log_out(self):
        wait = WebDriverWait(self.driver, 20)
        if self.driver.current_url == "https://www.saucedemo.com/inventory.html":
            print("Успешно!!! Пользователь находится в магазине")
            bm_button = wait.until(
                (EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
            )
            bm_button.click()
            logout_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="logout_sidebar_link"]'))
            )
            logout_link.click()
            print('Успешно!!! Клик по кнопке "Logout" выполнен!')

            assert self.driver.current_url == "https://www.saucedemo.com/", (
                "Ошибка!!! Переход к форме аутентификации не выполнен"
            )
            print("Успешно!!! Выполнен переход на страницу аутентификации!")
        else:
            print("Пользователь не находится на главной странице магазина!")
            print("Logout не требуется")
            self.clear_auth_form()


class PageUtils:
    """
    Класс со вспомогательными методами
    """

    def __init__(self):
        pass

    @staticmethod
    # Функция отбражения времени
    def print_test_time(begin_text):
        print("\n************************************************")
        print(f"{begin_text} {datetime.datetime.now().time().strftime('%H:%M:%S')} !!!")
        print("************************************************\n")


class TestCaseUserAuth:
    """
    Тесткейс для тестирования сценариев аутентификации
    пользователя интернет магазина
    """

    def __init__(self):
        pass

    def test_start(self):
        with webdriver.Chrome(options=options) as driver:
            # Начало теста
            PageUtils.print_test_time(
                "Начало тестирования основного аутентификации пользователя магазина {base_url}"
            )

            # Открытие браузера
            driver.get(base_url)
            driver.maximize_window()

            test_auth_page = TestAuthPage(driver, base_url)

            for login in login_list:
                print(f"Тест пользователя - {login}")
                time.sleep(2)
                test_auth_page.login_market(login, pwd)
                time.sleep(2)
                test_auth_page.check_auth(login)
                time.sleep(2)
                test_auth_page.log_out()

            time.sleep(5)

            # Завершение теста
            PageUtils.print_test_time("Успешное завершение теста")


test_case_user_auth = TestCaseUserAuth()
test_case_user_auth.test_start()

# test_case_smoke = TestCaseSmoke()
# test_case_smoke.test_start()

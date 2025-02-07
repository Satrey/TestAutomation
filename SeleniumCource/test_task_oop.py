# Сайт для теста QA 'demoqa.com' ,
# https://www.lambdatest.com/selenium-playground/jquery-dropdown-search-demo
# https://www.lambdatest.com/selenium-playground/

from itertools import product
import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Utils:
    """Вспомогательные функции"""

    def __init__(self):
        pass

    # Функция добавления товаров в корзину и проверки товаров находящихся в корзине и summory
    def test_cart(num: int, items, text: str):
        item_list = {}
        for i, item in enumerate(items, start=1):
            if i == num:
                product_name = item.find_element(By.CLASS_NAME, "inventory_item_name")
                product_price = item.find_element(By.CLASS_NAME, "inventory_item_price")
                if text == "Add to cart":
                    item.find_element(By.TAG_NAME, "button").click()
                    print(
                        f"Добавили товар {product_name.text} с ценой {product_price.text} в корзину"
                    )
                    item_list[product_name.text] = product_price.text.strip("$")
                else:
                    item_list[product_name.text] = product_price.text.strip("$")
                    print(
                        f"Добавили товар {product_name.text} с ценой {product_price.text} в список"
                    )
        return item_list

    # Функция для посчета общей стоимости корзины
    def cart_total(products: dict):
        cart_total = 0.0
        for price in products.values():
            cart_total += float(price)
        return round(cart_total, 2)


class TestAutentification:
    """Класс для аутентификации пользователя в интернет магазине"""

    def __init__(self, driver, base_url, login, password):
        self.driver = driver
        self.base_url = base_url
        self.login = login
        self.password = password

    """Метод аутентификации пользователя на сайте магазина"""

    def login_market(self):
        # Заполняем поле логин
        field_login = self.driver.find_element(By.ID, "user-name")
        field_login.send_keys(self.login)

        # Заполняем поле пароль
        field_password = self.driver.find_element(By.ID, "password")
        field_password.send_keys(self.password)

        # Нажимаем кнопку входа
        button_login = self.driver.find_element(By.ID, "login-button")
        button_login.click()

        # Проверка входа в магазин по логотипу
        logo_text = self.driver.find_element(By.XPATH, '//span[@class="title"]')
        assert logo_text.text == "Products", (
            "Неудача!!! Переход на главную страницу магазина не осуществлен!"
        )
        print("Успешно!!! Переход на главную страницу выполнен!")

        # Проверка входа в магазин по URL
        assert self.driver.current_url == "https://www.saucedemo.com/inventory.html", (
            "Неудача!!! Переход на главную страницу магазина не осуществлен!"
        )
        print(
            f"Успешно!!! Переход на главную страницу выполнен по адресу {driver.current_url}!"
        )


class TestAddProductToCart:
    """Класс"""

    def __init__(self, products):
        self.products = products

    # Метод для иммитации выбора конкретного товара пользователем
    def input_product(self):
        print("Выберите номер товара, который хотите добавить в корзину!")
        for i, product in enumerate(self.products, start=1):
            print(
                f"{i}. {product.find_element(By.CLASS_NAME, 'inventory_item_name').text}"
            )
        while True:
            try:
                product_number = int(input("Введите номер товара (1 - 6): "))
                if 1 <= product_number <= 6:
                    return product_number
                else:
                    print("Введите целое число из диапазона от 1 до 6 включительно")
            except ValueError:
                print("Ввод не является целым числом от 1 до 6, повторите попытку")

    # Метод добавления товаров в корзину и проверки товаров находящихся в корзине и summory
    def test_cart(self, num, products, text):
        item_list = {}
        for i, item in enumerate(products, start=1):
            if i == num:
                product_name = item.find_element(By.CLASS_NAME, "inventory_item_name")
                product_price = item.find_element(By.CLASS_NAME, "inventory_item_price")
                if text == "Add to cart":
                    item.find_element(By.TAG_NAME, "button").click()
                    print(
                        f"Добавили товар {product_name.text} с ценой {product_price.text} в корзину"
                    )
                    item_list[product_name.text] = product_price.text.strip("$")
                else:
                    item_list[product_name.text] = product_price.text.strip("$")
                    print(
                        f"Добавили товар {product_name.text} с ценой {product_price.text} в список"
                    )
        return item_list


# Параметры и опции драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument('--headless')

# # Учетные данные для входа в интернет магазиин
base_url = "https://www.saucedemo.com/"
login = "standard_user"
pwd = "secret_sauce"


with webdriver.Chrome(options=options) as driver:
    print("\n************************************************")
    print(f"Начало теста {datetime.datetime.now().time().strftime('%H:%M:%S')} !!!")
    print("************************************************\n")

    # Открытие браузера
    driver.maximize_window()
    driver.get(base_url)

    # Аутентификация пользователя
    ta = TestAutentification(driver, base_url, login, pwd)
    ta.login_market()

    inventory_list = driver.find_elements(By.CLASS_NAME, "inventory_item")

    tap = TestAddProductToCart(inventory_list)
    product_num = tap.input_product()
    print(f"Товар под номером - {product_num} выбран для добавления в корзину!")

    time.sleep(10)

    print("\n************************************************")
    print(
        f"Тест успешно завершен {datetime.datetime.now().time().strftime('%H:%M:%S')} !!!"
    )
    print("************************************************")

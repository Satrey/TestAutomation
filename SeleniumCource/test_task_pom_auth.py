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
    """Класс для аутентификации пользователя в интернет магазине"""

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

    # Проверка входа в магазин по логотипу
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
        # Заполняем поле логин
        field_login = wait.until(EC.element_to_be_clickable((By.ID, "user-name")))
        field_login.send_keys(Keys.CONTROL + "a")
        field_login.send_keys(Keys.BACKSPACE)

        # Заполняем поле пароль
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


class TestMarketPage:
    """Класс для тестирования главной страницы магазина"""

    def __init__(self, driver):
        self.driver = driver

    def get_inventory_list(self):
        wait = WebDriverWait(self.driver, 10)
        # Получение списка элементов на главной странице магазина
        inventory_list = wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )
        return inventory_list

    def select_products(self):
        inventory_list = self.get_inventory_list()
        selected_products = PageUtils.input_product(inventory_list)
        return selected_products

    def add_to_cart(self, num: int):
        inventory_list = self.get_inventory_list()
        items_list = PageUtils.processing_cart(num, inventory_list, "Add to cart")
        print("Товар добавлен в корзину - ", items_list)
        return items_list

    def check_products(self, items: dict):
        wait = WebDriverWait(self.driver, 10)
        print("Проверка продукта")
        print(
            f"Наименование добавленного продукта: {[p for p in items.keys()]} - \
              цена добавленного продукта: {[v for v in items.values()]}"
        )

        # Проверка количества товара в корзине по бейджу у иконки корзины
        cart_bage = wait.until(
            EC.visibility_of_element_located(
                ((By.XPATH, '//*[@id="shopping_cart_container"]/a/span'))
            )
        )
        assert len(items) == int(cart_bage.text), (
            "Ошибка! Количество товара не совпадает"
        )
        print(f"Успешно!!! Количество товара в корзине {cart_bage.text}")

        # Проверка перехода в корзину получение кнопки корзина
        cart_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="shopping_cart_container"]/a')
            )
        )
        # Нажатие на кнопку корзина
        cart_button.click()
        print("Нажатие на кнопку корзина!")
        assert self.driver.current_url == "https://www.saucedemo.com/cart.html", (
            "Неудача!!! Переход в корзину не выполнен, несоответствие URL"
        )
        print(f"Успешно!!! Выполнен переход в корзину по {self.driver.current_url}")

        time.sleep(2)


class TestCartPage:
    """Класс для тестирования корзины магазина"""

    def __init__(self, driver):
        self.driver = driver

    # Метод для олучения списка элементов присутствующих в корзине
    def get_cart_list(self):
        wait = WebDriverWait(self.driver, 10)
        cart_list = wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "cart_item"))
        )
        return cart_list

    # Метод для обработки и проверки товаров в корзине
    def products_in_cart(self, num: int):
        inventory_list = self.get_cart_list()
        cart_list = PageUtils.processing_cart(num, inventory_list, "checkout")
        print("Товар в корзине - ", cart_list)
        return cart_list

    def check_cart(self, items: dict):
        print("Проверка корзины")
        print(
            f"Наименование продукта в корзине: {[p for p in items.keys()]} - \
              цена продукта в корзине: {[v for v in items.values()]}"
        )

    # Метод поиска и проверки кнопки "checkout" и перехода на страницу оформления
    def checkout(self):
        wait = WebDriverWait(self.driver, 10)
        checkout_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="checkout"]'))
        )

        # Проверка и нажатие кнопки 'Checkout' в корзине
        assert checkout_button, "Не найдена кнопка Checkout"
        checkout_button.click()
        print('Нажатие на кнопку "Checkout" выполнено успешно')

        # Проверка перехода на страницу оформления заказа по URL
        assert (
            self.driver.current_url
            == "https://www.saucedemo.com/checkout-step-one.html"
        ), "Ошибка перехода на страницу оформления заказа шаг 1!!!"
        print("Успешно!!! Переход на страницу оформления заказа шаг 1 выполнен!")


class TestInfoPage:
    """Класс тестирования страницы оформления товара (шфг-1)"""

    def __init__(self, driver, first_name: str, last_name: str, zip_code: int):
        self.driver = driver
        self.first_name = first_name
        self.last_name = last_name
        self.zip_code = zip_code

    # Метод для обработки формы оформления товара
    def processing_fields(self):
        wait = WebDriverWait(self.driver, 10)

        # Получение полей формы оформления заказа
        first_name_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="first-name"]'))
        )
        last_name_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="last-name"]'))
        )
        zip_code_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="postal-code"]'))
        )

        # Заполнение полей формы оформления заказа
        first_name_field.send_keys(self.first_name)
        last_name_field.send_keys(self.last_name)
        zip_code_field.send_keys(self.zip_code)
        print("Заполнение полей формы выполнено успешно!!!")

    # Метод получения кнопки "continue" и перехода на страницу оформления (шаг-2)
    def check_continue(self):
        wait = WebDriverWait(self.driver, 5)
        # Переход к оформлению заказа
        continue_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="continue"]'))
        )

        # Проверка кнопки "Continue"
        assert continue_button, "Не найдена кнопка Continue"
        continue_button.click()
        print('Нажатие на кнопку "Continue" выполнено успешно')

        # Проверка перехода на страницу оформления заказа шаг 2 по URL
        assert (
            self.driver.current_url
            == "https://www.saucedemo.com/checkout-step-two.html"
        ), "Ошибка перехода на страницу оформления заказа шаг 2!!!"
        print("Успешно!!! Переход на страницу оформления заказа шаг 2 выполнен!")


class TestSummaryPage:
    """Класс для тестирования страницы оформления заказа (шаг-2),
    проверки стоимости заказа и комиссии"""

    def __init__(self, driver):
        self.driver = driver

    # Метод для получения списка товаров на странице офформления (шаг-2)
    def get_summary_list(self):
        wait = WebDriverWait(self.driver, 10)
        summary_list = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item"))
        )
        return summary_list

    # Метод для обработки и проверки товаров на странице оформления (шаг-2)
    def products_in_summary(self, num: int):
        inventory_list = self.get_summary_list()
        summary_list = PageUtils.processing_cart(num, inventory_list, "finish")
        print("Проверка итогового списка")
        print("Товар в итоговом списке - ", summary_list)
        return summary_list

    def check_summary(self, items: dict):
        print("Проверка итогового списка")
        print(
            f"Наименование продукта в итоговом списке: {[p for p in items.keys()]} - \
              цена продукта в итоговом списке: {[v for v in items.values()]}"
        )

    # Метод рассчета общей стоимости товаров в корзине
    def calculate_total(self, items: dict):
        # Рассчет общей стоимости товаров в корзине
        total = PageUtils.cart_total(items)
        print(f"Общая стоимость товаров в корзине - {total}")
        return total

    # Метод для получения общей стоимости товаров в корзине
    def get_subtotal(self):
        wait = WebDriverWait(self.driver, 10)
        # Получение общей стоимости товаров в корзине без комиссии
        subtotal_in_cart = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_subtotal_label"))
        )
        subtotal = float(subtotal_in_cart.text.split("$")[1])
        print(f"Стоимость товаров без комиссии - {subtotal}")
        return subtotal

    # Метод для получения комиссии
    def get_tax(self):
        wait = WebDriverWait(self.driver, 10)
        # Получение значения комиссии
        tax_in_cart = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_tax_label"))
        )
        tax = float(tax_in_cart.text.split("$")[1])
        print(f"Комиссия составляет - {tax}")
        return tax

    # Метод получения полной стоимости заказа
    def get_summary_total(self):
        # Получение стоимости товаров включая комиссию
        total_in_cart = self.driver.find_element(By.CLASS_NAME, "summary_total_label")
        summary_total = float(total_in_cart.text.split("$")[1])
        print(f"Стоимость товаров включая комиссию составляет - {summary_total}")
        return summary_total


class TestFinishPage:
    """Класс для тестирования страницы завершения оформления заказа"""

    def __init__(self, driver):
        self.driver = driver

    def check_finish_page(self):
        finish = self.driver.find_element(By.ID, "finish")
        finish.click()
        print("Нажатие на кнопку finish!")

        # Проверка перехода на страницу завершения покупки
        assert (
            self.driver.current_url
            == "https://www.saucedemo.com/checkout-complete.html"
        ), "Ошибка перехода на страницу завершения покупки!!!"
        print("Успешно!!! Переход на страницу завершения покупки выполнен!")

    def check_return_to_home_page(self):
        wait = WebDriverWait(self.driver, 10)
        # Нажатие на кнопку возврата на домашнюю страницу
        back_home_page = wait.until(
            EC.element_to_be_clickable((By.ID, "back-to-products"))
        )
        back_home_page.click()
        print("Нажатие на кнопку возврата на домашнюю страницу!")

        time.sleep(2)

        # Проверка перехода на домашнюю страницу
        print(f"Переход на домашнюю страницу {self.driver.current_url}")
        assert self.driver.current_url == "https://www.saucedemo.com/inventory.html", (
            "Ошибка перехода на домашнюю страницу!!!"
        )
        print("Успешно!!! Переход на домашнюю страницу выполнен!")


class PageUtils:
    """Класс со вспомогательными методами"""

    def __init__(self):
        pass

    @staticmethod
    # Метод добавления товаров в корзину и проверки товаров находящихся в корзине и summory
    def processing_cart(num: int, items, text: str):
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

    @staticmethod
    # Функция для иммитации выбора конкретного товара пользователем
    def input_product(products):
        print("Выберите номер товара, который хотите добавить в корзину!")
        for i, product in enumerate(products, start=1):
            print(
                f"{i}. {product.find_element(By.CLASS_NAME, 'inventory_item_name').text}"
            )
        while True:
            try:
                product_number = int(input("Введите номер товара (1 - 6): "))
                if 1 <= product_number <= 6:
                    print(
                        f"Товар под номером - {product_number} выбран для добавления в корзину!"
                    )
                    return product_number
                else:
                    print("Введите целое число из диапазона от 1 до 6 включительно")
            except ValueError:
                print("Ввод не является целым числом от 1 до 6, повторите попытку")

    @staticmethod
    # Функция для посчета общей стоимости корзины
    def cart_total(products: dict):
        cart_total = 0.0
        for price in products.values():
            cart_total += float(price)
        return round(cart_total, 2)

    @staticmethod
    # Функция отбражения времени
    def print_test_time(begin_text):
        print("\n************************************************")
        print(f"{begin_text} {datetime.datetime.now().time().strftime('%H:%M:%S')} !!!")
        print("************************************************\n")


class TestCaseSmoke:
    """Тест основного функционала интернет магазина "https://www.saucedemo.com/" """

    def __init__(self):
        pass

    def test_start(self):
        with webdriver.Chrome(options=options) as driver:
            # Начало теста
            PageUtils.print_test_time(
                f"Начало тестирования основного функционала интернет магазина {base_url}"
            )

            # Открытие браузера
            driver.get(base_url)
            driver.maximize_window()

            # Тест страницы авторизации
            test_auth_page = TestAuthPage(driver, base_url)
            test_auth_page.login_market(login, pwd)
            test_auth_page.check_auth(login)

            # Тест основной страницы магазина (добавление товара в корзину)
            test_market_page = TestMarketPage(driver)
            selected_product = test_market_page.select_products()

            # Получаем список товаров добавленных в корзину
            items_list = test_market_page.add_to_cart(selected_product)

            # Проверяем список товаров добавленных в корзину
            test_market_page.check_products(items_list)

            time.sleep(2)

            # Тест страницы корзины
            test_cart_page = TestCartPage(driver)

            # Получение списка товаров в корзине
            cart_list = test_cart_page.products_in_cart(len(items_list))
            test_cart_page.check_cart(cart_list)

            # Проверка соответствия списков товаров добавленных в корзину
            # и присутствующих в корзине
            assert items_list == cart_list, (
                "Неудача!!! Наименования или цены товаров в корзине не соответствуют добавленым товарам!"
            )
            print(
                "Успешно!!! Наименования и цены товаров в корзине соответствуют добавленным!"
            )

            # Переход на страницу оформления заказа (Шаг-1)
            test_cart_page.checkout()

            time.sleep(2)

            # Тест страницы оформления заказа
            test_info_page = TestInfoPage(driver, "Alex", "Pokrashenko", 625043)

            # Заполнение полей страницы оформления заказа (Шаг-1)
            test_info_page.processing_fields()

            # Переход на страницу оформления заказа (шаг-2)
            test_info_page.check_continue()

            time.sleep(2)

            # Тест страницы оформления заказа (шаг - 2)
            test_summary_page = TestSummaryPage(driver)
            summary_list = test_summary_page.products_in_summary(len(cart_list))

            # Проверка соответствия списков товаров
            assert items_list == cart_list == summary_list, (
                "Неудача!!! Наименования или цены товаров в итоговом списке не соответствуют товарам в корзине!"
            )
            print(
                "Успешно!!! Наименования и цены товаров в итоговом списке соответствуют товарам в корзине!"
            )

            # Расчитываем общую стоимость товаров в корзине без комиссии
            total = test_summary_page.calculate_total(summary_list)
            subtotal = test_summary_page.get_subtotal()

            # Проверка общей стоимости товаров без комиссии
            assert total == subtotal, (
                "Ошибка!!! Общая стоимость товаров без комиссии не совпадает!"
            )
            print("успешно!!! Общая стоимость товаров без комиссии совпадает!")

            time.sleep(2)

            # Получаем значение комиссии
            tax = test_summary_page.get_tax()
            summary_total = test_summary_page.get_summary_total()

            # Проверка стоимости товаров включая комиссию
            assert round((total + tax), 2) == summary_total, (
                "Ошибка!!! Общая стоимость товаров включая комиссию не совпадает!"
            )
            print("Успешно!!! Общая стоимость товаров включая комиссию совпадает!")

            time.sleep(2)

            # Тест страницы завершения оформления заказа и переход на домашнюю страницу
            test_finish_page = TestFinishPage(driver)
            test_finish_page.check_finish_page()

            time.sleep(2)

            # Проверка перехода на домашнюю страницу магазина
            test_finish_page.check_return_to_home_page()

            time.sleep(2)

            # Завершение теста
            PageUtils.print_test_time("Успешное завершение теста")


class TestCaseUserAuth:
    """Тесткейс для тестирования сценариев аутентификации
    пользователя интернет магазина"""

    def __init__(self):
        pass

    def test_start(self):
        with webdriver.Chrome(options=options) as driver:
            # Начало теста
            PageUtils.print_test_time(
                f"Начало тестирования аутентификации пользователя магазина {base_url}"
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


test_case_smoke = TestCaseSmoke()
test_case_smoke.test_start()

test_case_user_auth = TestCaseUserAuth()
test_case_user_auth.test_start()

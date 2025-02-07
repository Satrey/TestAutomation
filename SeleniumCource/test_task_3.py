# Для запуска в фоновом режиме раскоментировать строку '# options.add_argument('--headless')'
# После основных действий установлены time.sleep(2) для удобства, можно удалить.

# Код с прошлого тестового задания почти не пришлось изменять, написана новая функция для
# обработки пользовательского ввода и поправлено условие в функции 'test_cart'

# Была запара при тестировании товара 'Sauce Labs Bike Light'(все остальные проходили нормально),
#  тест постоянно падал при проверке общей стоимости товара включая комиссию. Долго не мог понять в чем дело,
# но как оказалось общая цена имела значение не 10.79 а 10.790000000000001.

# В функцию 'input_product' добавлена обработка исключения 'ValueError' ,
# а также конструкция If - else, для проверки диапазона введенного значения.


import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

# Параметры и опции драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.add_argument('--headless')


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


# Функция для иммитации выбора конкретного товара пользователем
def input_product(products):
    print("Выберите номер товара, который хотите добавить в корзину!")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product.find_element(By.CLASS_NAME, 'inventory_item_name').text}")
    while True:
        try:
            product_number = int(input("Введите номер товара (1 - 6): "))
            if 1 <= product_number <= 6:
                return product_number
            else:
                print("Введите целое число из диапазона от 1 до 6 включительно")
        except ValueError:
            print("Ввод не является целым числом от 1 до 6, повторите попытку")


# Функция аутентификации пользователя на сайте магазина
def login_site(base_url: str, login: str, pwd: str):
    # Открываем броузер
    browser.get(base_url)
    browser.maximize_window()

    # Заполняем поле логин
    field_login = browser.find_element(By.ID, "user-name")
    field_login.send_keys(login)

    # Заполняем поле пароль
    field_password = browser.find_element(By.ID, "password")
    field_password.send_keys(pwd)

    # Нажимаем кнопку входа
    button_login = browser.find_element(By.ID, "login-button")
    button_login.click()


# Функция для посчета общей стоимости корзины
def cart_total(products: dict):
    cart_total = 0.0
    for price in products.values():
        cart_total += float(price)
    return round(cart_total, 2)


# Переменные
product_add_cart = {}
product_in_cart = {}
product_in_summary = {}
cart_amount = 2

# Учетные данные для входа в интернет магазиин
base_url = "https://www.saucedemo.com/"
login = "standard_user"
pwd = "secret_sauce"

# Основной цикл
with webdriver.Chrome(options=options) as browser:
    print("\n************************************************")
    print(
        f"Начало теста основного функционала магазина  {base_url} {
            datetime.datetime.now().time().strftime('%H:%M:%S')
        } !!!"
    )
    print("************************************************\n")

    login_site(base_url, login, pwd)

    # Получение списка элементов на главной странице магазина
    inventory_list = browser.find_elements(By.CLASS_NAME, "inventory_item")

    # Выбор товара добавляемого в корзину
    cart_amount = input_product(inventory_list)
    print(f"Товар под номером - {cart_amount} выбран для добавления в корзину!")

    # Добавление необходимого количества товаров в корзину
    product_add_cart = test_cart(cart_amount, inventory_list, "Add to cart")
    print("Product added to cart - ", product_add_cart)

    product_name_add_cart = [p for p in product_add_cart.keys()]
    product_price_add_cart = [v for v in product_add_cart.values()]

    time.sleep(2)

    # Проверка добавления товара по бейджу у иконки корзины
    cart_bage = browser.find_element(
        By.XPATH, '//*[@id="shopping_cart_container"]/a/span'
    )
    assert len(product_add_cart) == int(cart_bage.text), (
        "Ошибка! Количество товара не совпадает"
    )
    print(f"Успешно!!! Количество товара в корзине {cart_bage.text}")

    # Проверка перехода в корзину
    cart = browser.find_element(
        By.XPATH, '//*[@id="shopping_cart_container"]/a'
    ).click()
    assert browser.current_url == "https://www.saucedemo.com/cart.html", (
        "Неудача!!! Переход в корзину не выполнен, несоответствие URL"
    )
    print(f"Успешно!!! Выполнен переход в корзину по {browser.current_url}")

    time.sleep(2)

    # Проверка списка товаров в корзине
    cart_amount = len(product_add_cart)
    cart_list = browser.find_elements(By.CLASS_NAME, "cart_item")
    product_in_cart = test_cart(cart_amount, cart_list, "checkout")
    print("Product in cart - ", product_in_cart)

    product_name_in_cart = [p for p in product_in_cart.keys()]
    product_price_in_cart = [v for v in product_in_cart.values()]

    time.sleep(2)

    # Проверка соответствия добавленного товара
    assert product_name_add_cart == product_name_in_cart, (
        "Неудача!!! Наименования товаров в корзине не соответствуют добавленым товарам!"
    )
    print("Успешно!!! Наименования товаров в корзине соответствуют добавленным!")

    assert product_price_add_cart == product_price_in_cart, (
        "Неудача!!! Цены товаров в корзине не соответствуют добавленым товарам!"
    )
    print("Успешно!!! Цены товаров совпадают!")

    # Переход к оформлению заказа
    checkout_button = browser.find_element(By.XPATH, '//button[@id="checkout"]')

    # Проверка и нажатие кнопки 'Checkout' в корзине
    assert checkout_button, "Нет кнопки Checkout"
    checkout_button.click()
    print('Нажатие на кнопку "Checkout" выполнено успешно')

    time.sleep(2)

    # Проверка перехода на страницу оформления заказа по URL
    assert browser.current_url == "https://www.saucedemo.com/checkout-step-one.html", (
        "Ошибка перехода на страницу оформления заказа шаг 1!!!"
    )
    print("Успешно!!! Переход на страницу оформления заказа шаг 1 выполнен!")

    # Получение полей формы оформления заказа
    first_name = browser.find_element(By.XPATH, '//input[@id="first-name"]')
    last_name = browser.find_element(By.XPATH, '//input[@id="last-name"]')
    zip_code = browser.find_element(By.XPATH, '//input[@id="postal-code"]')

    # Заполнение полей формы оформления заказа
    first_name.send_keys("Alex")
    last_name.send_keys("Pokrashenko")
    zip_code.send_keys(625034)
    print("Заполнение полей формы выполнено успешно!!!")

    # Переход к оформлению заказа
    continue_button = browser.find_element(By.XPATH, '//input[@id="continue"]')

    # Проверка кнопки "Continue"
    assert continue_button, "Нет кнопки Continue"
    continue_button.click()
    print('Нажатие на кнопку "Continue" выполнено успешно')

    # Проверка перехода на страницу оформления заказа шаг 2 по URL
    assert browser.current_url == "https://www.saucedemo.com/checkout-step-two.html", (
        "Ошибка перехода на страницу оформления заказа шаг 2!!!"
    )
    print("Успешно!!! Переход на страницу оформления заказа шаг 2 выполнен!")

    time.sleep(2)

    # Проверка списка товаров
    summary_list = browser.find_elements(By.CLASS_NAME, "cart_item")
    product_in_summary = test_cart(cart_amount, summary_list, "finish")
    print(product_in_summary)

    product_name_in_summary = [p for p in product_in_summary.keys()]
    product_price_in_summary = [v for v in product_in_summary.values()]

    # Проверка наименований товаров и цен
    assert product_name_add_cart == product_name_in_cart == product_name_in_summary, (
        "Ошибка!!! Наименования товаров не совпадают!"
    )
    print("Успешно!!! Наименования товаров совпадают во всех списках!")
    assert (
        product_price_add_cart == product_price_in_cart == product_price_in_summary
    ), "Ошибка!!! Цены товаров не совпадают"
    print("Успешно!!! Цены товаров совпадают!")

    # Рассчет общей стоимости товаров в корзине
    total = cart_total(product_in_summary)
    print(f"Общая стоимость товаров в корзине - {total}")

    time.sleep(2)

    # Получение общей стоимости товаров в корзине без комиссии
    subtotal_in_cart = browser.find_element(By.CLASS_NAME, "summary_subtotal_label")
    subtotal = float(subtotal_in_cart.text.split("$")[1])
    print(f"Стоимость товаров без комиссии - {subtotal}")

    # Проверка общей стоимости товаров без комиссии
    assert total == subtotal, (
        "Ошибка!!! Общая стоимость товаров без комиссии не совпадает!"
    )
    print("успешно!!! Общая стоимость товаров без комиссии совпадает!")

    # Получение значения комиссии
    tax_in_cart = browser.find_element(By.CLASS_NAME, "summary_tax_label")
    tax = float(tax_in_cart.text.split("$")[1])
    print(f"Комиссия составляет - {tax}")

    # Получение стоимости товаров включая комиссию
    total_in_cart = browser.find_element(By.CLASS_NAME, "summary_total_label")
    summary_total = float(total_in_cart.text.split("$")[1])
    print(f"Стоимость товаров включая комиссию составляет - {summary_total}")

    # Проверка стоимости товаров включая комиссию
    assert round((total + tax), 2) == summary_total, (
        "Ошибка!!! Общая стоимость товаров включая комиссию не совпадает!"
    )
    print("Успешно!!! Общая стоимость товаров включая комиссию совпадает!")

    time.sleep(2)

    finish = browser.find_element(By.ID, "finish")
    finish.click()
    print("Нажатие на кнопку finish!")

    # Проверка перехода на страницу завершения покупки
    assert browser.current_url == "https://www.saucedemo.com/checkout-complete.html", (
        "Ошибка перехода на страницу завершения покупки!!!"
    )
    print("Успешно!!! Переход на страницу завершения покупки выполнен!")

    time.sleep(2)

    # Нажатие на кнопку возврата на домашнюю страницу
    back_home_page = browser.find_element(By.ID, "back-to-products")
    back_home_page.click()
    print("Нажатие на кнопку возврата на домашнюю страницу!")

    time.sleep(2)

    # Проверка перехода на домашнюю страницу
    print(f"Переход на домашнюю страницу {browser.current_url}")
    assert browser.current_url == "https://www.saucedemo.com/inventory.html", (
        "Ошибка перехода на домашнюю страницу!!!"
    )
    print("Успешно!!! Переход на домашнюю страницу выполнен!")

    time.sleep(2)

    print("\n************************************************")
    print(
        f"Тест успешно завершен {datetime.datetime.now().time().strftime('%H:%M:%S')}!!!"
    )
    print("************************************************")

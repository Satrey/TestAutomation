import time

from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
# options.add_argument('--headless')

with webdriver.Chrome(options=options) as browser:

    # Учетные данные для входа в интернет магазиин
    base_url = 'https://www.saucedemo.com/'
    login = 'standard_user'
    pwd = 'secret_sauce'

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

    # Проверка входа в магазин по логотипу
    logo_text = browser.find_element(By.XPATH, '//span[@class="title"]')
    assert logo_text.text == 'Products', 'Неудача!!! Переход на главную страницу магазина не осуществлен!'
    print('Успешно!!! Переход на главную страницу выполнен!')

    # Проверка входа в магазин по URL
    current_url = browser.current_url
    assert current_url == 'https://www.saucedemo.com/inventory.html', \
                        'Неудача!!! Переход на главную страницу магазина не осуществлен!'
    print(f'Успешно!!! Переход на главную страницу выполнен по адресу {current_url}!')

    # Попытка добавления товара в корзину
    product_1 = browser.find_element(By.XPATH, '//a[@id="item_0_title_link"]')
    product_1_price = browser.find_element(By.XPATH, '//*[@id="inventory_container"]/div/div[2]/div[2]/div[2]/div')
    product_1_add_to_cart = browser.find_element(By.ID, 'add-to-cart-sauce-labs-bike-light').click()
    product_1_value = product_1.text
    product_1_price_value = product_1_price.text
    print(product_1.text, ' ', product_1_price.text)

    # Проверка добавления товара по бейджу у иконки корзины
    cart_bage = browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span')
    assert 1 == int(cart_bage.text), 'Ошибка! Количество товара не совпадает'
    print(f'Успешно!!! Количество товара в корзине {cart_bage.text}')

    # Проверка перехода в корзину
    cart = browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()
    assert browser.current_url == 'https://www.saucedemo.com/cart.html', 'Неудача!!! Переход в корзину не выполнен, несоответствие URL'
    print(f'Успешно!!! Выполнен переход в корзину по {browser.current_url}')

    # Проверка соответствия добавленного товара
    cart_product = browser.find_element(By.XPATH, '//*[@id="item_0_title_link"]/div')
    cart_product_price = browser.find_element(By.XPATH, '//*[@id="cart_contents_container"]/div/div[1]/div[3]/div[2]/div[2]/div')
    print(cart_product.text, ' ', cart_product_price.text)

    assert cart_product.text == product_1_value, "Ошибка!!! Название товара в корзине не соответствует названию в магазине!"
    print(f'Успешно наименования соответствуют {cart_product.text}')

    assert cart_product_price.text == product_1_price_value, "Ошибка!!! Цена товара в корзине не соответствует цене в магазине!"
    print(f'Успешно цены совпадают {cart_product_price.text}')

    # Переход к оформлению заказа
    checkout = browser.find_element(By.XPATH, '//button[@id="checkout"]')
    checkout.click()
    assert browser.current_url == 'https://www.saucedemo.com/checkout-step-one.html', 'Ошибка перехода на страницу оформления заказа!!!'
    print('Успешно!!! Переход на страницу оформления заказа выполнен!')

    first_name = browser.find_element(By.XPATH, '//input[@id="first-name"]')
    last_name = browser.find_element(By.XPATH, '//input[@id="last-name"]')
    zip_code = browser.find_element(By.XPATH, '//input[@id="postal-code"]')

    first_name.send_keys('Alex')
    last_name.send_keys('Pokrashenko')
    zip_code.send_keys(625034)

    time.sleep(10)


    # base_url = 'https://parsinger.ru/selenium/1/1.html'
    # browser.get(base_url)

    # first_name = browser.find_element(By.NAME, 'first_name')
    # last_name = browser.find_element(By.NAME, 'last_name')
    # middle_name = browser.find_element(By.NAME, 'patronymic')
    # age = browser.find_element(By.NAME, 'age')
    # city = browser.find_element(By.NAME, 'city')
    # email =browser.find_element(By.NAME, 'email')
    # btn = browser.find_element(By.ID, 'btn')

    # first_name.send_keys('Alexander')
    # last_name.send_keys('Pokrashenko')
    # middle_name.send_keys('Georgievich')
    # age.send_keys(46)
    # city.send_keys('Tyumen')
    # email.send_keys('satrey.mail@gmail.com')

    # time.sleep(2)
    # btn.click()

    # result = browser.find_element(By.ID, 'result')
    # print(f'Результат выполнения сценария на странице : {result.text}')

    # time.sleep(10)



    # browser.close()
    print('Тест завершен')


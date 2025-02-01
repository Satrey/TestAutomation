import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.select import Select

# Параметры и опции драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
# options.add_argument('--headless')

# Учетные данные для входа в интернет магазиин
base_url = 'https://www.saucedemo.com/'
login = 'standard_user'
pwd = 'secret_sauce'

# URL страниц сайта
home_page = 'https://www.saucedemo.com/inventory.html'

# elements = []

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

    # Проверка перехода на главную страницу магазина
    assert browser.current_url == home_page, \
                                  'Ошибка!!! Переход на главную страницу не выполнен, несоответствие URL'
    print(f'Успешно!!! Переход на главную страницу {home_page}')


# Функция для тестирования списка сортировки, не работает,
# вылетает на тесте 3го элемента списка с ошибкой 
# 'stale element not found in the current frame'

def sort_testing(element):
    select = Select(element)
    for i, item in enumerate(select.options, start=1):
        print(f'{i}. Выбор сортировки по - {item.text}')
        select.select_by_visible_text(item.text)
        time.sleep(5)


with webdriver.Chrome(options=options) as browser:

    print('\n************************************************')
    print(f'Начало теста {datetime.datetime.now().time().strftime('%H:%M:%S')}')
    print('************************************************\n')

    login_site(base_url, login, pwd)

    action = ActionChains(browser)
    
    # Функция для прохода по списку элементов фильтра сортировки в цикле 
    # sort_testing(element)

    # Проверка первого элемента списка сортировки
    element = browser.find_element(By.XPATH, '//select[@ class="product_sort_container"]')
    select = Select(element)
    select.select_by_visible_text('Name (A to Z)')
    print('Сортировка по Name (A to Z)')
    time.sleep(2)

    # Проверка второго элемента списка сортировки
    element = browser.find_element(By.XPATH, '//select[@ class="product_sort_container"]')
    select = Select(element)
    select.select_by_visible_text('Name (Z to A)')
    print('Сортировка по Name (Z to A)')
    time.sleep(2)

    # Проверка третьего элемента списка сортировки
    element = browser.find_element(By.XPATH, '//select[@ class="product_sort_container"]')
    select = Select(element)
    select.select_by_visible_text('Price (low to high)')
    print('Сортировка по Price (low to high)')
    time.sleep(2)

    # Проверка четвертого элемента списка сортировки
    element = browser.find_element(By.XPATH, '//select[@ class="product_sort_container"]')
    select = Select(element)
    select.select_by_visible_text('Price (high to low)')
    print('Сортировка по Price (high to low)')
    time.sleep(2)

    # time.sleep(5)

    print('\n************************************************')
    print(f'Тест успешно завершен {datetime.datetime.now().time().strftime('%H:%M:%S')}')
    print('************************************************')
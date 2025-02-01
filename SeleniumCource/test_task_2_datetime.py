import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Параметры и опции драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
# options.add_argument('--headless')

with webdriver.Chrome(options=options) as browser:

    print('\n************************************************')
    print(f'Начало теста {datetime.datetime.now().time().strftime('%H:%M:%S')} !!!')
    print('************************************************\n')

    # Получение текущей и создание новой даты
    current_date = datetime.datetime.now()
    print(f'Текущая дата - {current_date.strftime('%m/%d/%Y')}')
    new_date = current_date + datetime.timedelta(days=10)
    print(f'Текущая дата + 10 дней - {new_date.strftime('%m/%d/%Y')}')
    

    browser.get('https://demoqa.com/date-picker')
    browser.maximize_window()

    dt = browser.find_element(By.XPATH, '//input[@id="datePickerMonthYearInput"]')
    print(f'Значение в поле при открытии страницы - {dt.get_attribute('value')}')
    for i in range(20):
        dt.send_keys(Keys.BACKSPACE)

    dt.send_keys(new_date.strftime('%m/%d/%Y'))
    dt.send_keys(Keys.ENTER)
    print(f'Значение в поле после ввода - {dt.get_attribute('value')}')

    assert dt.get_attribute('value') == new_date.strftime('%m/%d/%Y'), 'Ошибка!!! Некорректная дата!'
    print('Успешно!!! Поле содержит верную дату!')

    print('\n************************************************')
    print(f'Тест успешно завершен {datetime.datetime.now().time().strftime('%H:%M:%S')} !!!')
    print('************************************************')
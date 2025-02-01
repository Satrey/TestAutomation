# Сайт для теста QA 'demoqa.com' , 

import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# Параметры и опции драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
# options.add_argument('--headless')

with webdriver.Chrome(options=options) as browser:

    print('\n************************************************')
    print(f'Начало теста основного функционала магазина {time.time()}!!!')
    print('************************************************\n')

    time.sleep(2)

    print('\n************************************************')
    print('Тест успешно завершен!!!')
    print('************************************************')
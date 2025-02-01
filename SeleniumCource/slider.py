import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Параметры и опции драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
# options.add_argument('--headless')

with webdriver.Chrome(options=options) as browser:

    print('\n************************************************')
    print(f'Начало теста {datetime.datetime.now().time().strftime('%H:%M:%S')} !!!')
    print('************************************************\n')

    action = ActionChains(browser)
    browser.maximize_window()
    browser.get('https://demoqa.com/slider')
    slider = browser.find_element(By.XPATH, '//input[@ class="range-slider range-slider--primary"]')

    action.click_and_hold(slider)
    action.move_by_offset(200,0)
    action.move_by_offset(-100,0)
    action.move_by_offset(-250,0)

    action.release()
    action.perform()

    slider_value = slider.get_attribute('value')
    print(slider_value)

    time.sleep(5)

    print('\n************************************************')
    print(f'Тест успешно завершен {datetime.datetime.now().time().strftime('%H:%M:%S')} !!!')
    print('************************************************')
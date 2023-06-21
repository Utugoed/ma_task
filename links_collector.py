import os
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


target_url = "https://www.auchan.ru/catalog/morozhenoe/plombir/"


driver_path = os.path.abspath('/usr/bin/chromedriver/home/willyam/code/python/ma_task/ma_task/drivers/chromedriver')
service = webdriver.chrome.service.Service(executable_path=driver_path)

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')

user_agent = UserAgent().chrome

driver = webdriver.Chrome(options=options, service=service)


cookies = {
    'region_id': '1',
    'merchant_ID_': '1',
    'methodDelivery_': '1',
    '_GASHOP': '001_Mitishchi',
    'rrpvid': '770996873268121',
    '_userGUID': '0:lj4bwxbm:rDGYlVPZ9bZjR0LBQf5UuWsxfKpprPGY',
    'rcuid': '6491ab597016a2f896df205a',
    'digi_uc': 'W1sidiIsIjcxNDA4OSIsMTY4NzM0NzkwMTg3N10sWyJ2IiwiNTIzMzIiLDE2ODczNDc1NDA4NjldLFsidiIsIjgyODI4MiIsMTY4NzM0Mzg1NzExN10sWyJ2IiwiNjkxNjc1IiwxNjg3MzM2NTY0NTQ0XV0=',
    'acceptCookies_': 'true',
    'rrlevt': '1687347902588',
    'rrviewed': '52332%2C691675%2C828282%2C714089',
    'qrator_jsid': '1687347066.642.mAwFdgmfMj7TCQVl-mk8v35r2kh48dam91o6o2gvl8612dj8g',
    '_dvs': '0:lj5mvpyp:xknCdVz5w7Q5LG8v0XCIL7PYpeoEjEms',
    'dSesn': '13d6cd97-001e-dbf8-6bcf-7fd0910f04c7',
}

product_card_class_name = 'css-n9ebcy-Item'
product_link_class_name = 'css-3d15b0'

try:
    driver.get(url=target_url)
    for cookie_name, cookie_value in cookies.items():
        driver.add_cookie({'name': cookie_name, 'value': cookie_value})

    item_links = []
    for i in range(1, 6):
        page_url = target_url + f'?page={i}'
        driver.get(url=page_url)
        time.sleep(1)
        
        item_link_elements = driver.find_elements(by=By.CLASS_NAME, value=product_link_class_name)
        item_links += [link.get_attribute('href') for link in item_link_elements]

    item_links = list(set(item_links))

finally:
    driver.close()
    driver.quit()

with open('links_msc', 'w') as file:
    for link in item_links:
        file.write(link + '\n')

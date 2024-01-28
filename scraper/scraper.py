from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json

def get_elements(driver, div_xpath, element_tag, pages_count) -> list[dict] :
    data = []
    for count in range(pages_count):
        cars = driver.find_element(By.XPATH, div_xpath)
        for element in cars.find_elements(By.TAG_NAME, element_tag):
            list_descriptions = [item.text for item in element.find_element(By.CLASS_NAME, 'css-1fe6w6s.e162wx9x0').find_elements(By.TAG_NAME, 'span')]
            single_element = {
                'name': element.find_element(By.TAG_NAME, 'span').text,
                'description': ''.join(list_descriptions),
                'price': element.find_element(By.CLASS_NAME, 'css-46itwz.e162wx9x0').text
            }
            data.append(single_element)
        if count > 1:
            btn_next_page = driver.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[1]/div[1]/div[6]/div/div[2]/div/div/a')
            btn_next_page.click()
    return data

def process_data(driver, pages_count, file_name: str = 'data'):
    elements = get_elements(driver, '/html/body/div[2]/div[5]/div[1]/div[1]/div[6]/div/div[1]', 'a', pages_count)
    with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(elements, json_file, ensure_ascii=False, indent=4)    


def run(pages_count):
    driver = webdriver.Chrome()
    driver.get('https://auto.drom.ru/bmw/')
    assert 'БМВ' in driver.title
    process_data(driver, pages_count)
    driver.close()
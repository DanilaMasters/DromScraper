from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import asyncio

async def get_products(page, search_text, selector, get_product):
    product_divs = await page.query_selector_all(selector)
    valid_products = []
    words = search_text.split(" ")

    async with asyncio.TaskGroup() as tg:
        for div in product_divs:
            async def task(p_div):
                product = await get_product(p_div)

                if not product["price"] or not product["url"]:
                    return

                for word in words:
                    if not product["name"] or word.lower() not in product["name"].lower():
                        break
                else:
                    valid_products.append(product)
            tg.create_task(task(div))

    return valid_products

async def get_product(element):
    list_descriptions = [item.text for item in element.find_element(By.CLASS_NAME, 'css-1fe6w6s.e162wx9x0').find_elements(By.TAG_NAME, 'span')]
    product = {
        'name': element.find_element(By.TAG_NAME, 'span').text,
        'description': ''.join(list_descriptions),
        'price': element.find_element(By.CLASS_NAME, 'css-46itwz.e162wx9x0').text
    }
    return product

async def get_elements(driver, div_xpath, next_page_xpath, tag, search_text, pages_count) -> list[dict] :
    valid_products = []
    words = search_text.split(" ")

    async with asyncio.TaskGroup() as tg:
        for count in range(pages_count):
            product_divs = driver.find_elements(By.CLASS_NAME, 'css-1oas0dk.e1huvdhj1')
            for div in product_divs:
                async def task(div):
                    product = await get_product(div)
                    if not product["price"]:
                        return None
                    for word in words:
                        if not product["name"] or word.lower() not in product["name"].lower():
                            break
                    else:
                        valid_products.append(product)
                tg.create_task(task(div))
            if count > 1:
                btn_next_page = driver.find_element(By.XPATH, next_page_xpath)
                btn_next_page.click()

    return valid_products

async def process_data(driver, search_text, pages_count, file_name: str = 'data'):
    elements = await get_elements(driver, '/html/body/div[2]/div[5]/div[1]/div[1]/div[6]/div/div[1]',
                             '/html/body/div[2]/div[5]/div[1]/div[1]/div[6]/div/div[2]/div/div/a', 'a', search_text, pages_count)
    for element in elements:
        print(element)
    with open(f'{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(elements, json_file, ensure_ascii=False, indent=4)    


async def run(pages_count, search_text):
    driver = webdriver.Chrome()
    driver.get('https://auto.drom.ru/bmw/')
    assert 'БМВ' in driver.title
    await process_data(driver, search_text, pages_count)
    driver.close()
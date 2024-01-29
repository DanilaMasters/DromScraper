import asyncio
from playwright.async_api import async_playwright
import json
import os
from .drom import get_product as get_drom_product
from requests import post

DROM = "https://auto.drom.ru/toyota/all"

URLS = {
    DROM: {
        "search_field_query": 'input[placeholder="Марка"]',
        "search_button_query": 'input[value="Go"]',
        "product_selector": "a.css-1oas0dk.e1huvdhj1",
        "next_page_url": "/page2"
    }
}

available_urls = URLS.keys()


# def load_auth():
#     FILE = os.path.join("Scraper", "auth.json")
#     with open(FILE, "r") as f:
#         return json.load(f)

# # place your bright data credentials in auth.json file with keys: "username", "password" and "host"
# cred = load_auth()
# auth = f'{cred["username"]}:{cred["password"]}'
# browser_url = f'wss://{auth}@{cred["host"]}'


async def search(metadata, page, search_text):
    # await page.goto(f'{page.url}{search_text}/page1')
    await page.goto(f'{page.url}{search_text}/page1')
    print(f"Searching for {search_text} on {page.url}")
    await page.wait_for_load_state()
    return page


async def get_products(page, search_text, divs_selector, next_page_url, get_product, page_count):
    print("Retreiving products.")
    valid_products = []
    words = search_text.split(" ")

    async with asyncio.TaskGroup() as tg:
        product_divs = await page.query_selector_all(divs_selector)
        for count in range(page_count):
            for div in product_divs:
                async def task(div):
                    product = await get_product(div)

                    if not product["price"] or not product["url"]:
                        return

                    for word in words:
                        if not product["name"] or word.lower() not in product["name"].lower():
                            break
                    else:
                        valid_products.append(product)
                tg.create_task(task(div))
            if count > 1:
                print(f'{page.url}{next_page_url}')
                await page.goto(f'{page.url}{next_page_url}')
                await page.wait_for_load_state()

    return valid_products


def save_results(results):
    data = {"results": results}
    # FILE = os.path.join("Scraper", "results.json")
    with open('results.json', "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def post_results(results, endpoint, search_text, source):
    headers = {
        "Content-Type": "application/json"
    }
    data = {"data": results, "search_text": search_text, "source": source}

    print("Sending request to", endpoint)
    response = post("http://localhost:8000" + endpoint,
                    headers=headers, json=data)
    print("Status code:", response.status_code)


async def main(url, search_text, response_route, page_count):
    metadata = URLS.get(url)
    if not metadata:
        print("Invalid URL.")
        return

    async with async_playwright() as pw:
        print('Connecting to browser.')
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        print("Connected.")
        await page.goto(url, timeout=120000)
        print("Loaded initial page.")
        # search_page = await search(metadata, page, search_text)
        search_page = page

        def func(x): return None
        if url == DROM:
            func = get_drom_product
        else:
            raise Exception('Invalid URL')

        results = await get_products(search_page, search_text, metadata["product_selector"], metadata["next_page_url"], func, page_count)
        print("Saving results.")
        post_results(results, response_route, search_text, url)

        await browser.close()

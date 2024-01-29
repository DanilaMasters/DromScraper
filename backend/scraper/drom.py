from asyncio import gather


async def get_stock(product_div):
    elements = await product_div.query_selector_all('.a-size-base')
    filtered_elements = [element for element in elements if 'stock' in await element.inner_text()]
    return filtered_elements


async def get_product(product_div):
    # Query for all elements at once
    # image_element_future = product_div.query_selector('img.s-image')
    # name_element_future = product_div.query_selector(
    #     'h2 a span')
    # price_element_future = product_div.query_selector('span.a-offscreen')
    # url_element_future = product_div.query_selector(
    #     'a.a-link-normal.s-no-hover.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')

    product_href = await product_div.get_attribute('href')
    product_img = await product_div.query_selector(selector='img.css-9w7beg.evrha4s0')
    product_info = None
    if product_img:
        product_info = await product_img.get_attribute('alt')

    # Await all queries at once
    # product_href, product_img, product_info = await gather(
    #     product_href_future,
    #     product_img_future,
    #     product_info_future,
    # )

    # Fetch all attributes and text at once

    return {"info": product_info, "href": product_href}

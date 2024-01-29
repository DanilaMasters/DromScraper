def trim_price(raw_price: str):
    price = ''
    for ch in raw_price:
        if ch.isdigit():
            price += ch
    return price

async def get_product(product_div):
    product_url = await product_div.get_attribute('href')
    product_img = await product_div.query_selector(selector='img.css-9w7beg.evrha4s0')
    product_img_src = await product_img.get_attribute('data-src')
    product_name_tag = await product_div.query_selector(selector='span[data-ftid=bull_title]')
    product_name = await product_name_tag.inner_text()
    product_price_tag = await product_div.query_selector(selector='span[data-ftid=bull_price]')
    product_price_raw = await product_price_tag.inner_text()
    product_price = trim_price(product_price_raw)

    return {'name': product_name, 'img': product_img_src, 'url': product_url, 'price': product_price}

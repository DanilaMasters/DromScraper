from fastapi import Request
from fastapi.routing import APIRouter
from web_app.app.products.dao import ProductDAO

router = APIRouter(prefix='/products', tags=['Producsts'])

@router.get('/all-results')
async def get_results():
    results = await ProductDAO.find_all()
    product_results = []
    for result in results:
        product_results.append({
            'name': result.name,
            'img': result.img,
            'url': result.url,
            'price': result.price
        })

    return product_results

@router.get('/show-results')
async def get_product_results(search_text: str):
    results = await ProductDAO.find_all(search_text=search_text.lower())
    return results

@router.post('/results')
async def submit_results(request: Request):
    data = await request.json()
    results = data.get('data')
    search_text = data.get("search_text").lower()
    source = data.get("source")

    for result in results:
        name = result.get('name')
        img = result.get('img')
        url = result.get('url')
        price = result.get('price')
        await ProductDAO.add(
            name=name,
            img=img,
            url=url,
            price=int(price),
            search_text=search_text,
            source=source
        )
    response = {'message': 'Received data successfully'}
    return response
    
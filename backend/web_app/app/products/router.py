from fastapi import Request
from fastapi.routing import APIRouter
from web_app.app.products.dao import ProductDAO

router = APIRouter(prefix='/products', tags=['Producsts'])

@router.get('/show-results')
async def get_product_results(search_text: str):
    results = ProductDAO.find_all(search_text=search_text)
    return results

@router.post('/results')
async def submit_results(request: Request):
    data = await request.json()
    results = data.get('data')
    response = []
    for result in results:
        info = result.get('info')
        href = result.get('href')
        item = await ProductDAO.find_one_or_none(href=href)
        if not item:
            await ProductDAO.add(info=info, href=href)
        else:
            response.append({'message': f'Item {info} with href: {href} already exists'})
    print(response if response is not None else {'message': 'Added succesfully!'})
    
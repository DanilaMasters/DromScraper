from fastapi.routing import APIRouter

from app.app.products.dao import ProductDAO

router = APIRouter(prefix='/products', tags=['Producsts'])

@router.get('/results')
async def get_product_results(search_text: str):
    results = ProductDAO.find_all(search_text=search_text)
    return results
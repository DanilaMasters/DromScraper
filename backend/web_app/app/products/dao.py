from web_app.app.dao.dao import BaseDAO
from web_app.app.products.models import ProductsResult, TrackedProducts

class ProductDAO(BaseDAO):
    model = ProductsResult

        
class TracketProductDAO(BaseDAO):
    model = TrackedProducts
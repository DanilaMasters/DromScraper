from app.app.dao import BaseDAO
from app.app.products.models import ProductsResult, TrackedProducts

class ProductDAO(BaseDAO):
    model = ProductsResult

class TracketProductDAO(BaseDAO):
    model = TrackedProducts
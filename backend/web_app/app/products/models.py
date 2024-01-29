from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from web_app.database import Base


class ProductsResult(Base):
    __tablename__ = 'products_results'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(1000), nullable=False)
    img = Column(String(1000))
    url = Column(String(1000))
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    search_text = Column(String(255))
    source = Column(String(255))


class TrackedProducts(Base):
    __tablename__ = 'tracked_products'
    
    id =Column(Integer, primary_key=True)
    name =Column(String(1000), nullable=False)
    created_at =Column(DateTime, default=datetime.utcnow, nullable=False)
    tracked =Column(Boolean, default=True)
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from app.models._utils import utcnow
from database.connection import Base


class Product(Base):
    """Produto da Shopee (ou outra plataforma)"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    original_price = Column(Float)
    sale_price = Column(Float)
    discount = Column(Integer)  # % de desconto
    image_url = Column(String(500))
    affiliate_url = Column(String(500), nullable=False)
    short_url = Column(String(100))
    category = Column(String(100))
    shopee_item_id = Column(String(100), unique=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utcnow)

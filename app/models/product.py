from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import relationship

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

    # Relacionamentos (somente leitura). O banco não tem FOREIGN KEY nessas colunas,
    # por isso o vínculo é declarado com foreign() sem alterar o schema.
    clicks = relationship(
        "Click",
        primaryjoin="Product.id == foreign(Click.product_id)",
        back_populates="product",
        viewonly=True,
    )
    posts = relationship(
        "Post",
        primaryjoin="Product.id == foreign(Post.product_id)",
        back_populates="product",
        viewonly=True,
    )

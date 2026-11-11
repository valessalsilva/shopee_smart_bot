"""Acesso a dados de produtos"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def _active_query(self, category: Optional[str] = None):
        query = self.session.query(Product).filter(Product.active == True)  # noqa: E712
        if category:
            query = query.filter(Product.category == category)
        return query

    def list_active(self, category: Optional[str] = None, newest_first: bool = False) -> list:
        query = self._active_query(category)
        if newest_first:
            query = query.order_by(Product.created_at.desc())
        return query.all()

    def count_active(self) -> int:
        return self._active_query().count()

    def list_categories(self) -> list:
        """Categorias distintas (de todos os produtos), sem vazios"""
        rows = self.session.query(Product.category).distinct().all()
        return [row[0] for row in rows if row[0]]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.query(Product).filter(Product.id == product_id).first()

    def exists_shopee_item(self, shopee_item_id: str) -> bool:
        return (
            self.session.query(Product).filter(Product.shopee_item_id == shopee_item_id).first()
            is not None
        )

    def add(self, product: Product, commit: bool = True) -> Product:
        self.session.add(product)
        if commit:
            self.session.commit()
        return product

    def commit(self):
        self.session.commit()

"""Acesso a dados de produtos (SQLAlchemy ORM)"""
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def _active_query(self, category: Optional[str] = None):
        query = self.session.query(Product).filter_by(active=True)
        if category:
            query = query.filter_by(category=category)
        return query

    def list_active(
        self,
        category: Optional[str] = None,
        newest_first: bool = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list:
        query = self._active_query(category)
        if newest_first:
            query = query.order_by(Product.created_at.desc())
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all()

    def count_active(self) -> int:
        return self._active_query().count()

    def get_random_active(self) -> Optional[Product]:
        """Sorteia um produto ativo direto no banco (sem carregar todos em memória)"""
        return self._active_query().order_by(func.random()).limit(1).first()

    def list_categories(self) -> list:
        """Categorias distintas (de todos os produtos), sem vazios"""
        rows = self.session.query(Product.category).distinct().all()
        return [row[0] for row in rows if row[0]]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.get(Product, product_id)

    def exists_shopee_item(self, shopee_item_id: str) -> bool:
        return self.session.query(Product.id).filter_by(shopee_item_id=shopee_item_id).first() is not None

    def add(self, product: Product, commit: bool = True) -> Product:
        self.session.add(product)
        if commit:
            self.session.commit()
        return product

    def commit(self):
        self.session.commit()

"""Camada de acesso a dados"""
from app.repositories.click_repository import ClickRepository
from app.repositories.product_repository import ProductRepository

__all__ = ["ClickRepository", "ProductRepository"]

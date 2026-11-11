"""
API JSON (útil para integrações).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories import ClickRepository, ProductRepository
from database import get_db

router = APIRouter(prefix="/api")


@router.get("/products")
async def api_products(category: str = None, db: Session = Depends(get_db)):
    """Lista de produtos ativos"""
    products = ProductRepository(db).list_active(category)
    return {
        "count": len(products),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "original_price": p.original_price,
                "sale_price": p.sale_price,
                "discount": p.discount,
                "image": p.image_url,
                "link": p.affiliate_url,
                "short_link": p.short_url,
                "category": p.category,
            }
            for p in products
        ],
    }


@router.get("/stats")
async def api_stats(db: Session = Depends(get_db)):
    """Estatísticas"""
    return {
        "total_products": ProductRepository(db).count_active(),
        "total_clicks": ClickRepository(db).count(),
    }

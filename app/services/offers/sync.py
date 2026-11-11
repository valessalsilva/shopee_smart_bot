"""
Sincronização de ofertas da Shopee para o banco local.
"""
import asyncio
import logging

from app.models import Product
from app.repositories import ProductRepository
from app.services.shopee import shopee
from database import get_session

logger = logging.getLogger(__name__)


def offer_to_product(offer: dict) -> Product:
    """Converte uma oferta da API da Shopee em Product"""
    product = Product(
        name=offer.get("productName", "Produto"),
        original_price=float(offer.get("originalPrice", 0) or 0),
        sale_price=float(offer.get("salePrice", 0) or 0),
        image_url=offer.get("imageUrl", ""),
        affiliate_url=offer.get("offerLink", ""),
        shopee_item_id=str(offer.get("shopeeItemId") or offer.get("offerId")),
        category=offer.get("categoryName", ""),
    )
    if product.original_price and product.sale_price:
        product.discount = int((1 - product.sale_price / product.original_price) * 100)
    return product


def save_offers(offers: list) -> int:
    """Grava as ofertas novas (ignora as já existentes). Retorna quantas foram inseridas."""
    session = get_session()
    try:
        repo = ProductRepository(session)
        inserted = 0
        for offer in offers:
            product = offer_to_product(offer)
            # Evita duplicar
            if repo.exists_shopee_item(product.shopee_item_id):
                continue
            repo.add(product, commit=False)
            inserted += 1
        repo.commit()
        return inserted
    finally:
        session.close()


async def sync_shopee_offers():
    """Sincroniza ofertas da Shopee ao iniciar (se configurado)"""
    if not shopee.app_id or not shopee.secret:
        logger.warning("⚠️  Credenciais Shopee não configuradas. Pulando sincronização.")
        return

    try:
        offers = await asyncio.to_thread(shopee.get_offer_list, 1, 20)
        save_offers(offers)
        logger.info(f"✅ Sincronizadas {len(offers)} ofertas da Shopee")
    except Exception as e:
        logger.error(f"❌ Erro ao sincronizar Shopee: {e}")

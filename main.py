"""
Arquivo principal - inicializa tudo:
1. Site FastAPI (porta 8000)
2. Bot do Telegram
3. Agendador de postagens
4. Busca inicial de produtos da Shopee
"""
import asyncio
import logging
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app import app as fastapi_app
from services.telegram_bot import run_bot_async, build_application
from services.scheduler import start_scheduler, shutdown_scheduler
from services.shopee import shopee
from database import Product, get_session, init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def sync_shopee_offers():
    """Sincroniza ofertas da Shopee ao iniciar (se configurado)"""
    if not shopee.app_id or not shopee.secret:
        logger.warning("⚠️  Credenciais Shopee não configuradas. Pulando sincronização.")
        return

    try:
        offers = await asyncio.to_thread(shopee.get_offer_list, 1, 20)
        session = get_session()
        try:
            for offer in offers:
                item_id = str(offer.get("shopeeItemId") or offer.get("offerId"))
                # Evita duplicar
                existing = session.query(Product).filter(Product.shopee_item_id == item_id).first()
                if existing:
                    continue

                product = Product(
                    name=offer.get("productName", "Produto"),
                    original_price=float(offer.get("originalPrice", 0) or 0),
                    sale_price=float(offer.get("salePrice", 0) or 0),
                    image_url=offer.get("imageUrl", ""),
                    affiliate_url=offer.get("offerLink", ""),
                    shopee_item_id=item_id,
                    category=offer.get("categoryName", ""),
                )
                if product.original_price and product.sale_price:
                    product.discount = int((1 - product.sale_price / product.original_price) * 100)
                session.add(product)
            session.commit()
            logger.info(f"✅ Sincronizadas {len(offers)} ofertas da Shopee")
        finally:
            session.close()
    except Exception as e:
        logger.error(f"❌ Erro ao sincronizar Shopee: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup e shutdown da aplicação"""
    # Startup
    logger.info("🚀 Iniciando Divulgador Inteligente...")
    init_db()
    await sync_shopee_offers()
    start_scheduler()
    # Inicia bot do Telegram em background
    asyncio.create_task(run_bot_async())
    logger.info("✅ Tudo pronto! Acesse http://localhost:8000")
    yield
    # Shutdown
    shutdown_scheduler()
    logger.info("👋 Encerrando...")


# Reposiciona o lifespan no app do FastAPI
fastapi_app.router.lifespan_context = lifespan


if __name__ == "__main__":
    uvicorn.run(
        "main:fastapi_app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )

"""
Criação da aplicação FastAPI e ciclo de vida (startup/shutdown).
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import api, web
from database import init_db

logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: banco, Shopee, agendador e bot. Shutdown: para o agendador."""
    # Imports locais: só carregam as integrações quando a aplicação sobe de fato
    from app.services.offers.sync import sync_shopee_offers
    from app.services.scheduler import shutdown_scheduler, start_scheduler
    from app.services.telegram.bot import run_bot_async

    logger.info("🚀 Iniciando Divulgador Inteligente...")
    init_db()
    await sync_shopee_offers()
    start_scheduler()
    # Inicia bot do Telegram em background (referência guardada para não ser coletada)
    app.state.bot_task = asyncio.create_task(run_bot_async())
    logger.info("✅ Tudo pronto! Acesse http://localhost:8000")
    yield
    shutdown_scheduler()
    logger.info("👋 Encerrando...")


def create_app(with_background_services: bool = True) -> FastAPI:
    """Cria o app. Use with_background_services=False em testes (sem bot/agendador)."""
    app = FastAPI(
        title="Divulgador Inteligente - Site de Promoções",
        lifespan=lifespan if with_background_services else None,
    )

    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    app.include_router(web.router)
    app.include_router(api.router)
    return app

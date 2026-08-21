"""
Agendador de postagens automáticas em horários específicos.
Usa APScheduler para disparar o job em cada horário configurado.
"""
import random
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import settings
from database import Product, get_session
from services.post_builder import post_builder

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def pick_random_product() -> Product:
    """Seleciona um produto aleatório ativo para postar"""
    session = get_session()
    try:
        products = session.query(Product).filter(Product.active == True).all()
        if not products:
            return None
        return random.choice(products)
    finally:
        session.close()


async def job_post_product():
    """Job que posta um produto aleatório"""
    try:
        product = pick_random_product()
        if not product:
            logger.warning("Nenhum produto ativo para postar")
            return

        logger.info(f"📤 Postando produto: {product.name}")
        result = await post_builder.auto_post(product)
        logger.info(f"✅ Resultado: {result}")
    except Exception as e:
        logger.error(f"❌ Erro no job: {e}")


def configure_jobs():
    """Configura os jobs baseado nos horários do .env"""
    for time_str in settings.POST_SCHEDULE:
        try:
            hour, minute = time_str.split(":")
            hour, minute = int(hour), int(minute)
            scheduler.add_job(
                job_post_product,
                trigger=CronTrigger(hour=hour, minute=minute),
                id=f"post_{time_str}",
                replace_existing=True,
                name=f"Postar às {time_str}",
            )
            logger.info(f"⏰ Agendado: postar às {time_str}")
        except ValueError:
            logger.error(f"Horário inválido: {time_str}")


def start_scheduler():
    """Inicia o agendador"""
    configure_jobs()
    scheduler.start()
    logger.info("✅ Agendador de postagens iniciado")


def shutdown_scheduler():
    scheduler.shutdown(wait=False)


def get_next_runs() -> list:
    """Retorna os próximos horários agendados"""
    jobs = scheduler.get_jobs()
    return [
        {"name": j.name, "next_run": j.next_run_time.isoformat() if j.next_run_time else None}
        for j in jobs
    ]

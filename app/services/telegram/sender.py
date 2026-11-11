"""
Envio de postagens para os chats do Telegram.
"""
import logging

from telegram import Bot

from config import settings

logger = logging.getLogger(__name__)

bot_instance: Bot = None


async def send_post(photo_url: str, caption: str) -> dict:
    """Envia uma postagem para todos os chats configurados"""
    global bot_instance
    if bot_instance is None:
        bot_instance = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    results = []
    for chat_id in settings.TELEGRAM_CHAT_IDS:
        try:
            msg = await bot_instance.send_photo(
                chat_id=chat_id,
                photo=photo_url,
                caption=caption[:1024],  # limite do Telegram
                parse_mode="HTML",
            )
            results.append({"chat_id": chat_id, "message_id": msg.message_id, "ok": True})
        except Exception as e:
            logger.error(f"Erro ao enviar para {chat_id}: {e}")
            results.append({"chat_id": chat_id, "error": str(e), "ok": False})
    return {"results": results}

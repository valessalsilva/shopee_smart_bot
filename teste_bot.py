
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telegram import Bot

load_dotenv(Path(__file__).resolve().parent / ".env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_IDS")

async def testar_bot():
    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="🎉 Olá! O Valessa Ofertas está funcionando! 🛍️"
    )

    print("Mensagem enviada com sucesso!")

if __name__ == "__main__":
    asyncio.run(testar_bot())

"""
Teste manual do bot: envia uma mensagem de boas-vindas ao TELEGRAM_CHAT_IDS.
Uso (na raiz do projeto): python scripts/teste_bot.py
"""
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telegram import Bot

# Carregar variáveis do .env (na raiz do projeto)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_IDS")

async def testar_bot():
    bot = Bot(token=TOKEN)

    mensagem = (
        "🛍️✨ SEJA MUITO BEM-VINDO(A) AOS ACHADINHOS DA VALESSA!\n\n"
        "Que bom ter você por aqui! ❤️\n\n"
        "🔥 Ofertas imperdíveis\n"
        "💰 Preços especiais\n"
        "😍 Produtos incríveis\n"
        "🛒 Achadinhos selecionados com carinho!\n\n"
        "Fique de olho e aproveite as oportunidades.\n\n"
        "❤️ Boas compras!"
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=mensagem
    )

    print("Mensagem enviada com sucesso!")

if __name__ == "__main__":
    asyncio.run(testar_bot())

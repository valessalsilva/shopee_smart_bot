"""
Configurações centralizadas do Divulgador Inteligente.
Carrega as variáveis do arquivo .env
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_IDS: list = [
        cid.strip() for cid in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if cid.strip()
    ]
    TELEGRAM_ADMIN_ID: int = int(os.getenv("TELEGRAM_ADMIN_ID", "0"))

    # Shopee
    SHOPEE_APP_ID: str = os.getenv("SHOPEE_APP_ID", "")
    SHOPEE_SECRET_KEY: str = os.getenv("SHOPEE_SECRET_KEY", "")

    # IA
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Bitly
    BITLY_TOKEN: str = os.getenv("BITLY_TOKEN", "")

    # Banco
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./divulgador.db")

    # Agendamento
    POST_SCHEDULE: list = [
        h.strip() for h in os.getenv("POST_SCHEDULE", "09:00,12:00,15:00,18:00,21:00").split(",")
    ]

    # Site
    SITE_URL: str = os.getenv("SITE_URL", "http://localhost:8000")


settings = Settings()

"""
Configurações centralizadas do Divulgador Inteligente.
Carrega as variáveis do arquivo .env da raiz do projeto.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Variáveis já definidas no ambiente têm prioridade sobre o .env
load_dotenv(BASE_DIR / ".env")


def split_csv(value: str) -> list:
    """Converte 'a, b,,c' em ['a', 'b', 'c']"""
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def to_int(value: str, default: int = 0) -> int:
    """Converte para int, usando o padrão quando vazio"""
    value = (value or "").strip()
    return int(value) if value else default


class Settings:
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_IDS: list = split_csv(os.getenv("TELEGRAM_CHAT_IDS", ""))
    TELEGRAM_ADMIN_ID: int = to_int(os.getenv("TELEGRAM_ADMIN_ID", "0"))

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
    POST_SCHEDULE: list = split_csv(
        os.getenv("POST_SCHEDULE", "09:00,12:00,15:00,18:00,21:00")
    )

    # Site
    SITE_URL: str = os.getenv("SITE_URL", "http://localhost:8000")


settings = Settings()

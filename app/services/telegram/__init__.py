"""Integração com o Telegram (envio de posts + comandos do bot)"""
from app.services.telegram.sender import send_post

__all__ = ["send_post"]

"""
Arquivo principal - inicializa tudo:
1. Site FastAPI (porta 8000)
2. Bot do Telegram
3. Agendador de postagens
4. Busca inicial de produtos da Shopee
"""
import logging

import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from app.factory import create_app  # noqa: E402

fastapi_app = create_app()
app = fastapi_app


if __name__ == "__main__":
    uvicorn.run(
        "main:fastapi_app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )

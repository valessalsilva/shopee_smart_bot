"""
Configuração dos testes.
Executado antes de qualquer import da aplicação: usa um banco SQLite temporário
e credenciais vazias, para nunca tocar no divulgador.db nem chamar APIs reais.
"""
import os
import tempfile
from pathlib import Path

_TMP_DIR = tempfile.mkdtemp(prefix="shopee_bot_tests_")
TEST_DB = Path(_TMP_DIR) / "test.db"

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"
for _key in ("TELEGRAM_BOT_TOKEN", "OPENAI_API_KEY", "BITLY_TOKEN", "SHOPEE_APP_ID", "SHOPEE_SECRET_KEY"):
    os.environ[_key] = ""
os.environ["TELEGRAM_CHAT_IDS"] = "-100111,-100222"
os.environ["TELEGRAM_ADMIN_ID"] = "42"
os.environ["SITE_URL"] = "http://test.local"

import pytest  # noqa: E402

from database import Base, engine, get_session, init_db  # noqa: E402


@pytest.fixture(autouse=True)
def clean_db():
    """Banco limpo a cada teste"""
    init_db()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session():
    s = get_session()
    yield s
    s.close()


@pytest.fixture
def make_product(session):
    from app.models import Product

    def _make(**kwargs):
        data = dict(
            name="Fone Bluetooth",
            original_price=100.0,
            sale_price=60.0,
            discount=40,
            image_url="http://img/1.jpg",
            affiliate_url="https://shopee.com.br/produto-1",
            category="Eletrônicos",
        )
        data.update(kwargs)
        product = Product(**data)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    return _make


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from app.factory import create_app

    return TestClient(create_app(with_background_services=False))

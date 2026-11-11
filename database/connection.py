"""
Conexão com o banco de dados (SQLite local por padrão).
Único ponto do projeto que cria engine e sessões.
Os modelos ficam em app/models; as consultas, em app/repositories.
"""
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import settings

Base = declarative_base()

_connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Cria SOMENTE as tabelas que ainda não existem (instalação nova).
    Nunca apaga, recria ou altera tabelas existentes (create_all usa checkfirst).
    """
    import app.models  # noqa: F401  registra os modelos no Base.metadata

    Base.metadata.create_all(bind=engine, checkfirst=True)


def get_session() -> Session:
    """Sessão avulsa: quem chama é responsável por fechar (prefira session_scope)"""
    return SessionLocal()


@contextmanager
def session_scope() -> Iterator[Session]:
    """
    Sessão para serviços/bot/agendador:
        with session_scope() as session:
            ProductRepository(session).list_active()
    Faz rollback em caso de erro e sempre fecha a sessão.
    O commit fica a cargo dos repositories (comportamento já existente).
    """
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Iterator[Session]:
    """Dependência do FastAPI: uma sessão por requisição"""
    with session_scope() as session:
        yield session

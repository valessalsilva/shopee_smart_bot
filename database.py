"""
Modelos do banco de dados (SQLite local).
Persistência de produtos, postagens e cliques.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import settings

Base = declarative_base()


class Product(Base):
    """Produto da Shopee (ou outra plataforma)"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    original_price = Column(Float)
    sale_price = Column(Float)
    discount = Column(Integer)  # % de desconto
    image_url = Column(String(500))
    affiliate_url = Column(String(500), nullable=False)
    short_url = Column(String(100))
    category = Column(String(100))
    shopee_item_id = Column(String(100), unique=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    """Postagem enviada para o Telegram"""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    message_text = Column(Text, nullable=False)
    chat_id = Column(String(100), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)


class Click(Base):
    """Rastreamento de cliques nos links"""
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    short_code = Column(String(50), unique=True)
    user_ip = Column(String(50))
    user_agent = Column(String(255))
    clicked_at = Column(DateTime, default=datetime.utcnow)


# Inicialização
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Cria todas as tabelas"""
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()

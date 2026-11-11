from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models._utils import utcnow
from database.connection import Base


class Post(Base):
    """Postagem enviada para o Telegram"""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    message_text = Column(Text, nullable=False)
    chat_id = Column(String(100), nullable=False)
    sent_at = Column(DateTime, default=utcnow)
    clicks = Column(Integer, default=0)

    product = relationship(
        "Product",
        primaryjoin="foreign(Post.product_id) == Product.id",
        back_populates="posts",
        viewonly=True,
    )

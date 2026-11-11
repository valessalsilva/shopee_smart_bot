from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.models._utils import utcnow
from database.connection import Base


class Click(Base):
    """Rastreamento de cliques nos links"""
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    short_code = Column(String(50), unique=True)
    user_ip = Column(String(50))
    user_agent = Column(String(255))
    clicked_at = Column(DateTime, default=utcnow)

    product = relationship(
        "Product",
        primaryjoin="foreign(Click.product_id) == Product.id",
        back_populates="clicks",
        viewonly=True,
    )

from sqlalchemy import Column, DateTime, Integer, String

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

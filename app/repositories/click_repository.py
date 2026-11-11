"""Acesso a dados de links curtos / cliques (SQLAlchemy ORM)"""
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.models import Click


class ClickRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_code(self, code: str, with_product: bool = False) -> Optional[Click]:
        query = self.session.query(Click).filter_by(short_code=code)
        if with_product:
            query = query.options(joinedload(Click.product))
        return query.first()

    def code_exists(self, code: str) -> bool:
        return self.session.query(Click.id).filter_by(short_code=code).first() is not None

    def count(self) -> int:
        return self.session.query(Click).count()

    def create(self, code: str, product_id: Optional[int] = None) -> Click:
        click = Click(product_id=product_id, short_code=code, user_ip="", user_agent="")
        self.session.add(click)
        self.session.commit()
        return click

    def register_access(self, code: str, ip: str, user_agent: str) -> Optional[Click]:
        """Grava IP/User-Agent do acesso ao link. Retorna o Click ou None."""
        click = self.get_by_code(code)
        if click:
            click.user_ip = ip
            click.user_agent = user_agent
            self.session.commit()
        return click

"""Acesso a dados de links curtos / cliques"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Click


class ClickRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_code(self, code: str) -> Optional[Click]:
        return self.session.query(Click).filter(Click.short_code == code).first()

    def code_exists(self, code: str) -> bool:
        return self.get_by_code(code) is not None

    def count(self) -> int:
        return self.session.query(Click).count()

    def create(self, code: str, product_id: Optional[int] = None) -> Click:
        click = Click(product_id=product_id, short_code=code, user_ip="", user_agent="")
        self.session.add(click)
        self.session.commit()
        return click

    def commit(self):
        self.session.commit()

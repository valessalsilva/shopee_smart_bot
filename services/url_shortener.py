"""
Encurtador de URLs próprio + integração opcional com Bitly.
Cada link encurtado rastreia cliques.
"""
import string
import random
import requests
from sqlalchemy.orm import Session
from database import Click, get_session
from config import settings


class URLShortener:
    def __init__(self):
        self.bitly_token = settings.BITLY_TOKEN

    def _generate_code(self, length: int = 7) -> str:
        """Gera código aleatório para o link curto"""
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def shorten(self, original_url: str, product_id: int = None) -> str:
        """Encurta URL. Tenta Bitly primeiro, senão gera código próprio."""
        # 1. Tenta Bitly
        if self.bitly_token:
            try:
                short = self._shorten_bitly(original_url)
                if short:
                    return self._save_and_return(short, original_url, product_id)
            except Exception as e:
                print(f"[Bitly] Erro: {e}")

        # 2. Fallback: encurtador próprio
        return self._generate_own(original_url, product_id)

    def _shorten_bitly(self, url: str) -> str:
        """Encurta usando Bitly"""
        headers = {"Authorization": f"Bearer {self.bitly_token}"}
        data = {"long_url": url}
        response = requests.post(
            "https://api-ssl.bitly.com/v4/shorten",
            headers=headers,
            json=data,
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get("link", "")

    def _generate_own(self, original_url: str, product_id: int = None) -> str:
        """Gera link curto próprio (para usar com /r/{code})"""
        session: Session = get_session()
        try:
            for _ in range(10):  # tenta 10 vezes gerar código único
                code = self._generate_code()
                existing = session.query(Click).filter(Click.short_code == code).first()
                if not existing:
                    click = Click(
                        product_id=product_id,
                        short_code=code,
                        user_ip="",
                        user_agent="",
                    )
                    session.add(click)
                    session.commit()
                    return f"{settings.SITE_URL}/r/{code}"
            raise Exception("Não foi possível gerar código único")
        finally:
            session.close()

    def _save_and_return(self, short_url: str, original_url: str, product_id: int) -> str:
        """Salva encurtamento externo no banco"""
        session = get_session()
        try:
            code = short_url.split("/")[-1]
            click = Click(
                product_id=product_id,
                short_code=code,
                user_ip="",
                user_agent="",
            )
            session.add(click)
            session.commit()
            return short_url
        finally:
            session.close()

    def register_click(self, code: str, ip: str, user_agent: str) -> int:
        """Registra um clique e retorna o product_id"""
        session = get_session()
        try:
            click = session.query(Click).filter(Click.short_code == code).first()
            if click:
                click.user_ip = ip
                click.user_agent = user_agent
                click.clicked_at = click.clicked_at  # atualiza
                session.commit()
                return click.product_id or 0
            return 0
        finally:
            session.close()


shortener = URLShortener()

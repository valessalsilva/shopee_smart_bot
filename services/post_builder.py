"""
Serviço principal que monta a postagem de um produto.
Junta: produto + copy IA + link encurtado + imagem.
"""
from database import Product, get_session
from services.ai_copy import ai_copy
from services.url_shortener import shortener


class PostBuilder:
    """Constrói a mensagem final para o Telegram"""

    def __init__(self):
        self.ai = ai_copy
        self.shortener = shortener

    def build(self, product: Product, custom_text: str = None) -> dict:
        """Retorna dict com caption HTML + photo URL pronto pro Telegram"""
        # 1. Gera o texto (copy) se não foi passado
        if not custom_text:
            text = self.ai.generate(
                product_name=product.name,
                price=product.sale_price or product.original_price,
                original_price=product.original_price if product.sale_price else None,
            )
        else:
            text = custom_text

        # 2. Encurta URL
        short_url = product.short_url or self.shortener.shorten(
            product.affiliate_url, product_id=product.id
        )

        # 3. Monta o caption final
        caption = f"{text}\n\n🔗 {short_url}"

        return {
            "photo": product.image_url,
            "caption": caption,
            "short_url": short_url,
        }

    def auto_post(self, product: Product) -> dict:
        """Envia automaticamente para o Telegram"""
        from services.telegram_bot import send_post
        payload = self.build(product)
        return send_post(payload["photo"], payload["caption"])


post_builder = PostBuilder()

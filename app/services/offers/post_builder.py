"""
Serviço principal que monta a postagem de um produto.
Junta: produto + copy IA + link encurtado + imagem.
"""
from app.models import Product
from app.services.ai import ai_copy
from app.services.links import shortener
from app.services.telegram.sender import send_post


class PostBuilder:
    """Constrói a mensagem final para o Telegram"""

    def __init__(self):
        self.ai = ai_copy
        self.shortener = shortener

    def build(self, product: Product, custom_text: str = None) -> dict:
        """Retorna dict com caption HTML + photo URL pronto pro Telegram"""
        if not custom_text:
            text = self.ai.generate(
                product_name=product.name,
                price=product.sale_price or product.original_price,
                original_price=product.original_price if product.sale_price else None,
            )
        else:
            text = custom_text

        short_url = product.short_url or self.shortener.shorten(
            product.affiliate_url, product_id=product.id
        )

        caption = f"{text}\n\n🔗 {short_url}"

        return {
            "photo": product.image_url,
            "caption": caption,
            "short_url": short_url,
        }

    async def auto_post(self, product: Product) -> dict:
        """Envia automaticamente para o Telegram"""
        payload = self.build(product)
        return await send_post(payload["photo"], payload["caption"])


post_builder = PostBuilder()

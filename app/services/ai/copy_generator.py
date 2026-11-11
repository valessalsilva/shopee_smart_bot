"""
Gerador de textos de venda com IA (OpenAI).
Cria copy persuasivo com variações para teste A/B.
"""
import logging
import random

from openai import OpenAI

from config import settings

logger = logging.getLogger(__name__)


COPY_TEMPLATES = [
    {
        "name": "urgencia",
        "system": "Você é um copywriter especialista em e-commerce brasileiro. Crie textos de venda curtos, com senso de urgência, emojis estratégicos e gatilhos de escassez. Tom: empolgante, mas não apelativo. Máximo 280 caracteres.",
    },
    {
        "name": "beneficios",
        "system": "Você é um copywriter especializado em destacar benefícios de produtos. Crie textos que foquem em como o produto resolve problemas do cliente. Use linguagem simples e direta. Máximo 280 caracteres.",
    },
    {
        "name": "social_proof",
        "system": "Você é um copywriter focado em prova social. Crie textos que mencionam popularidade, avaliações positivas e que outras pessoas já estão aproveitando. Máximo 280 caracteres.",
    },
    {
        "name": "desconto",
        "system": "Você é um copywriter focado em promoções. Destaque o desconto, economia e a temporalidade da oferta. Use emojis de fogo/relâmpago. Máximo 280 caracteres.",
    },
]


class AICopyGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    def generate(self, product_name: str, price: float, original_price: float = None, style: str = None) -> str:
        """Gera um texto de venda para o produto"""
        if not self.client:
            return self._fallback_copy(product_name, price, original_price)

        # Escolhe um estilo aleatório se não informado
        template = next((t for t in COPY_TEMPLATES if t["name"] == style), random.choice(COPY_TEMPLATES))

        context = f"Produto: {product_name}\nPreço: R$ {price:.2f}"
        if original_price and original_price > price:
            discount = int((1 - price / original_price) * 100)
            context += f"\nDe: R$ {original_price:.2f}\nDesconto: {discount}%"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": template["system"]},
                    {"role": "user", "content": f"Crie uma postagem para o Telegram sobre:\n{context}"},
                ],
                max_tokens=150,
                temperature=0.8,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"[AI] Erro ao gerar copy: {e}")
            return self._fallback_copy(product_name, price, original_price)

    def generate_ab_variations(self, product_name: str, price: float, original_price: float = None, n: int = 3) -> list:
        """Gera N variações para teste A/B"""
        variations = []
        for _ in range(n):
            text = self.generate(product_name, price, original_price)
            variations.append(text)
        return variations

    def _fallback_copy(self, name: str, price: float, original_price: float = None) -> str:
        """Copy de fallback caso a IA não esteja disponível"""
        if original_price and original_price > price:
            discount = int((1 - price / original_price) * 100)
            return f"🔥 {name}\n\n💰 De R$ {original_price:.2f} por apenas R$ {price:.2f}\n⚡ {discount}% OFF\n\n🛒 Garanta o seu -> link abaixo"
        return f"✨ {name}\n\n💰 Apenas R$ {price:.2f}\n\n🛒 Aproveite -> link abaixo"


ai_copy = AICopyGenerator()

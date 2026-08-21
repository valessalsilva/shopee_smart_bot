"""
Integração com a API de Afiliados da Shopee.
Documentação: https://affiliate.shopee.com.br/
"""
import hashlib
import time
import requests
from config import settings


class ShopeeAffiliate:
    """Cliente para a API de Afiliados da Shopee"""

    BASE_URL = "https://open-api.affiliate.shopee.com.br/graphql"

    def __init__(self):
        self.app_id = settings.SHOPEE_APP_ID
        self.secret = settings.SHOPEE_SECRET_KEY

    def _generate_signature(self, payload: str, timestamp: int) -> str:
        """Gera a assinatura SHA256 exigida pela Shopee"""
        factor = f"{self.app_id}{timestamp}{payload}{self.secret}".encode("utf-8")
        return hashlib.sha256(factor).hexdigest()

    def _request(self, query: str, variables: dict = None) -> dict:
        """Faz uma requisição GraphQL para a Shopee"""
        import json
        payload = json.dumps({"query": query, "variables": variables or {}})
        timestamp = int(time.time())
        signature = self._generate_signature(payload, timestamp)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"SHA256 Credential={self.app_id}, Timestamp={timestamp}, Signature={signature}",
        }

        response = requests.post(self.BASE_URL, headers=headers, data=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_offer_list(self, page: int = 1, limit: int = 20) -> list:
        """Busca lista de ofertas/promoções disponíveis"""
        query = """
        query GetOfferList($page: Int, $limit: Int) {
            offerV2(page: $page, limit: $limit) {
                nodes {
                    offerId
                    categoryName
                    commissionRate
                    imageUrl
                    offerLink
                    originalPrice
                    salePrice
                    productName
                    shopeeItemId
                }
            }
        }
        """
        data = self._request(query, {"page": page, "limit": limit})
        return data.get("data", {}).get("offerV2", {}).get("nodes", [])

    def get_hot_deals(self, limit: int = 10) -> list:
        """Busca promoções quentes (em alta)"""
        query = """
        query GetHotDeals($limit: Int) {
            hotDeals(limit: $limit) {
                nodes {
                    itemId
                    itemName
                    itemUrl
                    imageUrl
                    originalPrice
                    salePrice
                    discount
                }
            }
        }
        """
        data = self._request(query, {"limit": limit})
        return data.get("data", {}).get("hotDeals", {}).get("nodes", [])

    def get_trending_products(self, category: str = None, limit: int = 20) -> list:
        """Busca produtos em alta, opcionalmente por categoria"""
        query = """
        query GetTrending($category: String, $limit: Int) {
            productOfferV2(listType: TRENDING, category: $category, limit: $limit) {
                nodes {
                    itemId
                    productName
                    productLink
                    imageUrl
                    price
                    priceDiscountRate
                    commissionRate
                }
            }
        }
        """
        data = self._request(query, {"category": category, "limit": limit})
        return data.get("data", {}).get("productOfferV2", {}).get("nodes", [])

    def convert_link(self, url: str) -> str:
        """Converte uma URL comum em link de afiliado"""
        query = """
        mutation ConvertLink($url: String!) {
            generateShortLink(input: {originUrl: $url}) {
                shortLink
            }
        }
        """
        data = self._request(query, {"url": url})
        return data.get("data", {}).get("generateShortLink", {}).get("shortLink", url)


shopee = ShopeeAffiliate()

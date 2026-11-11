import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from app.models import Product
from app.services.ai import ai_copy
from app.services.links import shortener
from app.services.offers import sync
from app.services.offers.post_builder import post_builder
from app.services.shopee import ShopeeAffiliate


def test_ai_fallback_without_key():
    assert ai_copy.client is None
    text = ai_copy.generate("Fone", 60.0, 100.0)
    assert "40% OFF" in text and "Fone" in text


def test_shortener_own_code_and_click():
    short = shortener.shorten("https://shopee.com.br/x", product_id=7)
    assert short.startswith("http://test.local/r/")
    code = short.rsplit("/", 1)[-1]
    assert shortener.register_click(code, "1.2.3.4", "pytest") == 7
    assert shortener.register_click("nope", "1.2.3.4", "pytest") == 0


def test_shopee_signature_is_sha256():
    client = ShopeeAffiliate()
    client.app_id, client.secret = "id", "secret"
    sig = client._generate_signature('{"q":1}', 1700000000)
    assert len(sig) == 64 and sig == client._generate_signature('{"q":1}', 1700000000)


def test_offer_to_product():
    p = sync.offer_to_product({
        "productName": "Tênis", "originalPrice": "200", "salePrice": "150",
        "imageUrl": "i", "offerLink": "l", "shopeeItemId": 99, "categoryName": "Moda",
    })
    assert p.shopee_item_id == "99" and p.discount == 25 and p.category == "Moda"


def test_save_offers_skips_duplicates(session):
    offers = [{"productName": "X", "offerLink": "l", "shopeeItemId": 1}]
    assert sync.save_offers(offers) == 1
    assert sync.save_offers(offers) == 0
    assert session.query(Product).count() == 1


def test_sync_skips_without_credentials():
    with patch.object(sync.shopee, "get_offer_list") as fake:
        asyncio.run(sync.sync_shopee_offers())
        fake.assert_not_called()


def test_post_builder_build(make_product):
    p = make_product(short_url="http://s/abc")
    payload = post_builder.build(p, custom_text="Oferta!")
    assert payload == {
        "photo": p.image_url,
        "caption": "Oferta!\n\n🔗 http://s/abc",
        "short_url": "http://s/abc",
    }


def test_auto_post_sends_to_all_chats(make_product):
    from app.services.telegram import sender

    p = make_product(short_url="http://s/abc")
    fake_bot = MagicMock()
    fake_bot.send_photo = AsyncMock(return_value=MagicMock(message_id=10))
    with patch.object(sender, "bot_instance", fake_bot):
        result = asyncio.run(post_builder.auto_post(p))
    assert [r["chat_id"] for r in result["results"]] == ["-100111", "-100222"]
    assert all(r["ok"] for r in result["results"])

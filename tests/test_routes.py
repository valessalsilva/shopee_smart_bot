from app.services.links import shortener


def test_home(client, make_product):
    make_product(name="Fone Top")
    r = client.get("/")
    assert r.status_code == 200
    assert "Fone Top" in r.text


def test_home_filter_category(client, make_product):
    make_product(name="Panela", category="Casa")
    make_product(name="Camisa", category="Moda")
    r = client.get("/?category=Casa")
    assert r.status_code == 200
    assert "Panela" in r.text and "Camisa" not in r.text


def test_product_detail(client, make_product):
    p = make_product(name="Mochila")
    assert client.get(f"/produto/{p.id}").status_code == 200
    assert client.get("/produto/9999").status_code == 404


def test_api_products_and_stats(client, make_product):
    make_product()
    data = client.get("/api/products").json()
    assert data["count"] == 1
    assert data["products"][0]["link"] == "https://shopee.com.br/produto-1"
    assert client.get("/api/stats").json() == {"total_products": 1, "total_clicks": 0}


def test_short_link_redirect(client, make_product):
    p = make_product()
    short = shortener.shorten(p.affiliate_url, product_id=p.id)
    code = short.rsplit("/", 1)[-1]

    r = client.get(f"/r/{code}", follow_redirects=False)
    assert r.status_code in (302, 307)
    assert r.headers["location"] == p.affiliate_url
    assert client.get("/r/naoexiste", follow_redirects=False).status_code == 404

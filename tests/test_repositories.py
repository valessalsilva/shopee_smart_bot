from app.repositories import ClickRepository, ProductRepository


def test_product_repository(session, make_product):
    make_product(name="A", category="Casa")
    make_product(name="B", category="Moda")
    make_product(name="C", category="Casa", active=False)
    repo = ProductRepository(session)

    assert {p.name for p in repo.list_active()} == {"A", "B"}
    assert [p.name for p in repo.list_active("Casa")] == ["A"]
    assert repo.count_active() == 2
    assert set(repo.list_categories()) == {"Casa", "Moda"}


def test_product_pagination_and_random(session, make_product):
    for i in range(5):
        make_product(name=f"P{i}")
    repo = ProductRepository(session)
    assert len(repo.list_active(limit=2)) == 2
    assert len(repo.list_active(limit=10, offset=3)) == 2
    assert repo.get_random_active().name.startswith("P")
    assert repo.exists_shopee_item("nao-existe") is False


def test_click_repository(session, make_product):
    p = make_product()
    repo = ClickRepository(session)
    repo.create(code="abc", product_id=p.id)
    assert repo.code_exists("abc")
    assert not repo.code_exists("zzz")
    assert repo.count() == 1

    click = repo.register_access("abc", "1.1.1.1", "ua")
    assert (click.user_ip, click.user_agent) == ("1.1.1.1", "ua")
    assert repo.register_access("zzz", "1.1.1.1", "ua") is None
    assert repo.get_by_code("abc", with_product=True).product.id == p.id

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


def test_click_repository(session):
    repo = ClickRepository(session)
    repo.create(code="abc", product_id=1)
    assert repo.code_exists("abc")
    assert not repo.code_exists("zzz")
    assert repo.count() == 1

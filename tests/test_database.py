import re

import pytest
from sqlalchemy import create_engine, inspect

from app.models import Click, Post, Product
from config import BASE_DIR
from database import Base, engine, init_db, session_scope


def test_tables_created():
    tables = set(inspect(engine).get_table_names())
    assert {"products", "posts", "clicks"} <= tables


def test_models_match_existing_divulgador_db():
    """Os models devem bater com o banco real, aberto SOMENTE LEITURA via SQLAlchemy."""
    db_path = BASE_DIR / "divulgador.db"
    if not db_path.exists():
        pytest.skip("divulgador.db não encontrado")

    ro_engine = create_engine(f"sqlite:///file:{db_path.as_posix()}?mode=ro&uri=true")
    try:
        real = inspect(ro_engine)
        for table in Base.metadata.sorted_tables:
            real_cols = {c["name"]: c for c in real.get_columns(table.name)}
            assert set(real_cols) == {c.name for c in table.columns}, table.name
            for col in table.columns:
                if not col.primary_key:
                    assert real_cols[col.name]["nullable"] == col.nullable, f"{table.name}.{col.name}"

            real_unique = {tuple(u["column_names"]) for u in real.get_unique_constraints(table.name)}
            model_unique = {(c.name,) for c in table.columns if c.unique}
            assert real_unique == model_unique, table.name

            # Os relacionamentos não podem ter criado FOREIGN KEY no schema
            assert real.get_foreign_keys(table.name) == []
            assert not table.foreign_keys
    finally:
        ro_engine.dispose()


def test_init_db_does_not_drop_existing_data(make_product):
    make_product(name="Persistente")
    init_db()
    init_db()
    with session_scope() as session:
        assert [p.name for p in session.query(Product).all()] == ["Persistente"]


def test_relationships(make_product):
    p = make_product()
    with session_scope() as session:
        session.add_all([
            Click(product_id=p.id, short_code="c1"),
            Click(product_id=p.id, short_code="c2"),
            Click(product_id=None, short_code="orfao"),
            Post(product_id=p.id, message_text="oi", chat_id="-100"),
        ])
        session.commit()

        product = session.get(Product, p.id)
        assert {c.short_code for c in product.clicks} == {"c1", "c2"}
        assert len(product.posts) == 1 and product.posts[0].product.id == p.id
        assert session.query(Click).filter_by(short_code="orfao").one().product is None

        joined = session.query(Click).join(Click.product).filter(Product.id == p.id).count()
        assert joined == 2


def test_session_scope_rolls_back_on_error():
    with pytest.raises(RuntimeError):
        with session_scope() as session:
            session.add(Product(name="X", affiliate_url="u"))
            session.flush()
            raise RuntimeError("falha")
    with session_scope() as session:
        assert session.query(Product).count() == 0


# Padrões montados por partes para este arquivo não casar consigo mesmo
_RAW_SQL = re.compile(
    "|".join([
        r"\bsqlite" + r"3\b",
        r"\btext" + r"\(\s*[\"']",
        r"exec_driver" + r"_sql",
        r"raw_" + r"connection",
        r"\.execute" + r"\(\s*[\"']",
        r"[\"']\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|PRAGMA)" + r"\s",
    ]),
    re.IGNORECASE,
)


def test_no_sql_files_or_raw_sql_in_project():
    ignored = {".git", "venv", ".venv", "__pycache__", ".pytest_cache"}
    files = [p for p in BASE_DIR.rglob("*") if not ignored & set(p.parts)]

    assert [p for p in files if p.suffix.lower() == ".sql"] == []

    offenders = []
    for path in files:
        if path.suffix == ".py":
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if _RAW_SQL.search(line):
                    offenders.append(f"{path.relative_to(BASE_DIR)}:{n}: {line.strip()}")
    assert offenders == []

import sqlite3

import pytest
from sqlalchemy import inspect

from config import BASE_DIR
from database import Base, engine


def test_tables_created():
    tables = set(inspect(engine).get_table_names())
    assert {"products", "posts", "clicks"} <= tables


def test_models_match_existing_divulgador_db():
    """O schema dos models deve bater com o banco real (aberto somente leitura)."""
    db_path = BASE_DIR / "divulgador.db"
    if not db_path.exists():
        pytest.skip("divulgador.db não encontrado")

    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        for table in Base.metadata.sorted_tables:
            real_cols = {row[1] for row in conn.execute(f"PRAGMA table_info({table.name})")}
            assert real_cols == {c.name for c in table.columns}, table.name
    finally:
        conn.close()

from config import settings
from config.settings import BASE_DIR, split_csv, to_int


def test_env_vars_loaded():
    assert settings.TELEGRAM_CHAT_IDS == ["-100111", "-100222"]
    assert settings.TELEGRAM_ADMIN_ID == 42
    assert settings.SITE_URL == "http://test.local"
    assert settings.DATABASE_URL.startswith("sqlite:///")
    assert "divulgador.db" not in settings.DATABASE_URL


def test_all_expected_settings_exist():
    for name in (
        "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_IDS", "TELEGRAM_ADMIN_ID", "SHOPEE_APP_ID",
        "SHOPEE_SECRET_KEY", "OPENAI_API_KEY", "BITLY_TOKEN", "DATABASE_URL",
        "POST_SCHEDULE", "SITE_URL",
    ):
        assert hasattr(settings, name)


def test_split_csv():
    assert split_csv(" a, b,,c ") == ["a", "b", "c"]
    assert split_csv("") == []
    assert split_csv(None) == []


def test_to_int_tolerates_empty():
    assert to_int("") == 0
    assert to_int("  ") == 0
    assert to_int("123") == 123


def test_base_dir_is_project_root():
    assert (BASE_DIR / "main.py").exists()

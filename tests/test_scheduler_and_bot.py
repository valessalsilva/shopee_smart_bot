from app.services.scheduler import jobs


def test_pick_random_product(make_product):
    assert jobs.pick_random_product() is None
    make_product(name="Único")
    assert jobs.pick_random_product().name == "Único"


def test_configure_jobs(monkeypatch):
    monkeypatch.setattr(jobs.settings, "POST_SCHEDULE", ["09:00", "invalido", "21:30"])
    jobs.scheduler.remove_all_jobs()
    jobs.configure_jobs()
    assert {j.id for j in jobs.scheduler.get_jobs()} == {"post_09:00", "post_21:30"}
    jobs.scheduler.remove_all_jobs()


def test_telegram_application_handlers(monkeypatch):
    from app.services.telegram import bot

    monkeypatch.setattr(bot.settings, "TELEGRAM_BOT_TOKEN", "123456:TEST-TOKEN")
    application = bot.build_application()
    commands = set()
    for handler in application.handlers[0]:
        commands |= set(getattr(handler, "commands", ()))
    assert {"start", "produtos", "novo", "stats"} <= commands


def test_main_module_exposes_app():
    from fastapi.testclient import TestClient

    import main

    # Sem "with": não dispara o lifespan (bot/agendador/Shopee)
    client = TestClient(main.fastapi_app)
    assert client.get("/").status_code == 200
    assert client.get("/api/stats").status_code == 200
    assert client.get("/produto/1").status_code == 404
    assert client.get("/r/x", follow_redirects=False).status_code == 404

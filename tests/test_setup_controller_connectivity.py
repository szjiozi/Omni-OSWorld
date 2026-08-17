import requests

from desktop_env.controllers import setup as controller_setup_module
from desktop_env.controllers.setup import SetupController


def test_setup_controller_retries_a_timed_out_health_probe(monkeypatch):
    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        if len(calls) == 1:
            raise requests.Timeout("not ready")
        return object()

    monkeypatch.setattr(controller_setup_module.requests, "get", fake_get)
    monkeypatch.setattr(
        controller_setup_module.time, "sleep", lambda _seconds: None
    )

    controller = SetupController("203.0.113.1")
    assert controller.setup([]) is True
    assert len(calls) == 2
    assert calls[0][1]["timeout"] == 10


def test_setup_controller_stops_after_bounded_health_retries(monkeypatch):
    calls = []

    def always_timeout(url, **kwargs):
        calls.append((url, kwargs))
        raise requests.Timeout("not ready")

    monkeypatch.setattr(
        controller_setup_module.requests, "get", always_timeout
    )
    monkeypatch.setattr(
        controller_setup_module.time, "sleep", lambda _seconds: None
    )

    controller = SetupController("203.0.113.1")
    assert controller.setup([]) is False
    assert len(calls) == controller_setup_module.MAX_RETRIES

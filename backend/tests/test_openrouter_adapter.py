import json
import pytest
import httpx
from app.services import openrouter
from app.core.config import get_settings

CANDIDATES = [{"id": 7, "name": "Demo gateway", "brand": "ExampleTech", "description": "Industrial gateway device", "category": "Industrial", "type": "Gateway", "subtype": "Vision"}]


@pytest.mark.asyncio
@pytest.mark.parametrize("app_origin", ["", "https://sales.example"])
async def test_openrouter_valid_json_and_authorization(monkeypatch, app_origin):
    monkeypatch.setenv("OPENROUTER_API_KEY", "fake-secret-only-for-test")
    monkeypatch.setenv("APP_ORIGIN", app_origin)
    get_settings.cache_clear()
    recorded = {}
    def handler(request: httpx.Request):
        recorded["auth"] = request.headers["authorization"]
        recorded["referer"] = request.headers.get("http-referer")
        recorded["data"] = json.loads(request.content)
        return httpx.Response(200, json={"choices": [{"message": {"content": '{"suggestions":[{"product_id":7,"reason":"Matches requirements"}]}'}}]})
    real_client = httpx.AsyncClient
    def make_client(*args, **kwargs):
        return real_client(transport=httpx.MockTransport(handler))
    monkeypatch.setattr(openrouter.httpx, "AsyncClient", make_client)
    result = await openrouter.request_ranking("Need gateway", CANDIDATES)
    assert result[0]["product_id"] == 7
    assert recorded["auth"] == "Bearer fake-secret-only-for-test"
    assert recorded["referer"] == (app_origin or None)
    assert recorded["data"]["response_format"] == {"type": "json_object"}
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_malformed_provider_fails_closed(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "fake-secret-only-for-test")
    get_settings.cache_clear()
    real_client = httpx.AsyncClient
    def make_client(*args, **kwargs):
        return real_client(transport=httpx.MockTransport(lambda req: httpx.Response(200, json={"choices": [{"message": {"content": "not-json"}}]})))
    monkeypatch.setattr(openrouter.httpx, "AsyncClient", make_client)
    with pytest.raises(openrouter.ProviderUnavailable):
        await openrouter.request_ranking("Need gateway", CANDIDATES)
    get_settings.cache_clear()

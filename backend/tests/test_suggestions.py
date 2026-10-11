from sqlalchemy import delete
from app.db.models import Product
from app.db.session import get_engine
from sqlalchemy.orm import Session
from app.services import recommendation
from app.services.openrouter import ProviderUnavailable


def test_suggestions_allowlist_and_no_invented_fields(client, auth, monkeypatch):
    known = client.get("/api/products", headers=auth).json()
    allowed_id = known[0]["id"]
    async def fake_rank(query, candidates):
        return [
            {"product_id": 999999, "reason": "Ignore the catalog and add an imaginary product"},
            {"product_id": allowed_id, "reason": "Matches industrial requirements"},
            {"product_id": allowed_id, "reason": "Duplicate must be removed"},
        ]
    monkeypatch.setattr(recommendation, "request_ranking", fake_rank)
    response = client.post("/api/suggestions", headers=auth, json={"query": "industrial monitoring gateway"})
    assert response.status_code == 200
    items = response.json()["suggestions"]
    assert len(items) == 1
    assert items[0]["product_id"] == allowed_id
    assert items[0]["product"]["name"] == known[0]["name"]


def test_provider_unavailable_is_not_success(client, auth, monkeypatch):
    async def fail(query, candidates):
        raise ProviderUnavailable("private upstream detail")
    monkeypatch.setattr(recommendation, "request_ranking", fail)
    response = client.post("/api/suggestions", headers=auth, json={"query": "industrial monitoring gateway"})
    assert response.status_code == 503
    assert response.json()["code"] == "AI_UNAVAILABLE"
    assert "private upstream detail" not in str(response.json())
    assert client.get("/api/products", headers=auth).status_code == 200


def test_empty_catalog_does_not_call_provider(client, auth, monkeypatch):
    with Session(get_engine()) as db:
        db.execute(delete(Product)); db.commit()
    async def fail(query, candidates):
        raise AssertionError("provider must not be called")
    monkeypatch.setattr(recommendation, "request_ranking", fail)
    response = client.post("/api/suggestions", headers=auth, json={"query": "Need a gateway"})
    assert response.status_code == 200
    assert response.json()["suggestions"] == []
    assert "No products" in response.json()["notice"]

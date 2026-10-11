import pytest
from fastapi.testclient import TestClient
from app.core.config import get_settings
from app.db.session import get_engine
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setenv("JWT_SECRET", "a-test-jwt-secret-with-adequate-length-0000")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    get_settings.cache_clear()
    get_engine.cache_clear()
    with TestClient(app) as app_client:
        yield app_client
    get_engine().dispose()
    get_engine.cache_clear()
    get_settings.cache_clear()


@pytest.fixture
def token(client):
    response = client.post("/api/auth/register", json={"username": "sampleuser", "email": "sample@example.test", "password": "test-password-123"})
    assert response.status_code == 201
    login = client.post("/api/auth/login", json={"username": "sampleuser", "password": "test-password-123"})
    assert login.status_code == 200
    return login.json()["access_token"]


@pytest.fixture
def auth(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def example_product():
    return {
        "name": "Demo Access Controller", "brand": "TestBrand", "description": "Controls secure industrial access with a redundant network link.",
        "category": "Security", "type": "Gateway", "subtype": "Access", "image_url": "https://example.test/product.png"
    }

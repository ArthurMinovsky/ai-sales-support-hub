from datetime import datetime, timedelta, timezone
import jwt
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.core.config import get_settings
from app.core.security import verify_password
from app.db.models import User
from app.db.session import get_engine
from app.main import app


def test_register_hash_and_duplicate(client):
    body = {"username": " NewUser ", "password": "long-strong-password", "confirm_password": "long-strong-password"}
    create = client.post("/api/auth/register", json=body)
    assert create.status_code == 201
    assert create.json()["username"] == "newuser"
    assert set(create.json()) == {"id", "username", "created_at"}
    with Session(get_engine()) as session:
        user = session.scalar(select(User).where(User.username == "newuser"))
        assert user.password_hash != body["password"]
        assert verify_password(body["password"], user.password_hash)
        assert "email" not in User.__table__.columns
    assert client.post("/api/auth/register", json=body).status_code == 409


@pytest.mark.parametrize("changes", [
    {"confirm_password": "different-password"},
    {"username": "invalid username"},
    {"password": "tiny-123", "confirm_password": "tiny-123"},
    {"password": "x" * 129, "confirm_password": "x" * 129},
    {"email": "unused@example.test"},
])
def test_registration_validation_never_returns_passwords(client, changes):
    body = {"username": "newperson", "password": "long-strong-password", "confirm_password": "long-strong-password"}
    body.update(changes)
    response = client.post("/api/auth/register", json=body)
    assert response.status_code == 422
    assert all("input" not in error and "ctx" not in error for error in response.json()["detail"])
    assert body["password"] not in response.text
    assert client.post("/api/auth/login", json={"username": "newperson", "password": body["password"]}).status_code == 401


def test_confirmation_is_required(client):
    assert client.post("/api/auth/register", json={"username": "newperson", "password": "long-strong-password"}).status_code == 422


def test_login_and_signed_3600_seconds(client):
    client.post("/api/auth/register", json={"username": "demo", "password": "longer-password-1", "confirm_password": "longer-password-1"})
    response = client.post("/api/auth/login", json={"username": " DEMO ", "password": "longer-password-1"})
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer" and data["expires_in"] == 3600
    claims = jwt.decode(data["access_token"], get_settings().jwt_secret, algorithms=["HS256"])
    assert claims["exp"] - claims["iat"] == 3600
    assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"}).status_code == 200
    assert client.post("/api/auth/login", json={"username": "demo", "password": "wrong"}).status_code == 401


def test_protected_routes_reject_missing_forged_and_expired(client, token):
    for path in ["/api/auth/me", "/api/products"]:
        assert client.get(path).status_code == 401
        assert client.get(path, headers={"Authorization": "Bearer invalid"}).status_code == 401
    assert client.post("/api/suggestions", json={"query": "test gateway"}).status_code == 401
    claims = jwt.decode(token, get_settings().jwt_secret, algorithms=["HS256"])
    claims["exp"] = int((datetime.now(timezone.utc) - timedelta(minutes=2)).timestamp())
    expired = jwt.encode(claims, get_settings().jwt_secret, algorithm="HS256")
    headers = {"Authorization": f"Bearer {expired}"}
    assert client.get("/api/products", headers=headers).status_code == 401
    assert client.post("/api/suggestions", json={"query": "test gateway"}, headers=headers).status_code == 401


def test_previous_start_token_cannot_authorize_reused_user_id(tmp_path, monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "a-test-jwt-secret-with-adequate-length-0000")
    previous_token = None
    ids = []
    for database in ("before.db", "after.db"):
        get_engine().dispose()
        get_engine.cache_clear()
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / database}")
        get_settings.cache_clear()
        with TestClient(app) as client:
            body = {"username": "reusable", "password": "testing-password-123", "confirm_password": "testing-password-123"}
            created = client.post("/api/auth/register", json=body)
            assert created.status_code == 201
            ids.append(created.json()["id"])
            if previous_token:
                assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {previous_token}"}).status_code == 401
            previous_token = client.post("/api/auth/login", json={"username": "reusable", "password": body["password"]}).json()["access_token"]
            assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {previous_token}"}).status_code == 200
    assert ids == [1, 1]
    get_engine().dispose()
    get_engine.cache_clear()
    get_settings.cache_clear()

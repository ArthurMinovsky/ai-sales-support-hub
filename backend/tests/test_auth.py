from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import get_settings


def test_register_hash_and_duplicate(client):
    body = {"username": "NewUser", "email": "NEW@example.test", "password": "long-strong-password"}
    create = client.post("/api/auth/register", json=body)
    assert create.status_code == 201
    assert create.json()["username"] == "newuser"
    assert "password" not in create.json() and "password_hash" not in create.json()
    assert client.post("/api/auth/register", json=body).status_code == 409
    assert client.post("/api/auth/register", json={**body, "email": "bad-address"}).status_code == 422


def test_login_and_signed_3600_seconds(client):
    client.post("/api/auth/register", json={"username": "demo", "email": "demo@example.test", "password": "longer-password-1"})
    response = client.post("/api/auth/login", json={"username": "demo", "password": "longer-password-1"})
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

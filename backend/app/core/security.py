from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi import HTTPException, status
from app.core.config import get_settings

hasher = PasswordHash.recommended()
JWT_TTL_SECONDS = 3600


def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(plaintext: str, stored_hash: str) -> bool:
    return hasher.verify(plaintext, stored_hash)


def issue_token(user_id: int) -> str:
    secret = get_settings().jwt_secret
    if len(secret) < 32:
        raise RuntimeError("JWT_SECRET must contain 32+ characters")
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "iat": now, "exp": now + timedelta(seconds=JWT_TTL_SECONDS)}, secret, algorithm="HS256")


def decode_token(token: str) -> int:
    try:
        data = jwt.decode(token, get_settings().jwt_secret, algorithms=["HS256"], options={"require": ["exp", "iat", "sub"]})
        return int(data["sub"])
    except (InvalidTokenError, ValueError, KeyError, TypeError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session", headers={"WWW-Authenticate": "Bearer"}) from exc

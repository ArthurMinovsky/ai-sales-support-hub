from datetime import datetime
from typing import Annotated
from email_validator import validate_email
from pydantic import AfterValidator, BaseModel, Field, field_validator


def normalize_email(value: str) -> str:
    candidate = value.strip()
    try:
        return validate_email(
            candidate,
            check_deliverability=False,
            test_environment=candidate.lower().endswith(".test"),
        ).normalized.lower()
    except ValueError as exc:
        raise ValueError(str(exc)) from exc


EmailAddress = Annotated[
    str,
    AfterValidator(normalize_email),
    Field(json_schema_extra={"format": "email"}),
]


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailAddress
    password: str = Field(min_length=10, max_length=128)

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        return value.strip().lower()

class LoginRequest(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    username: str
    email: EmailAddress
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductFields(BaseModel):
    name: str = Field(min_length=1, max_length=180)
    brand: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=10, max_length=6000)
    image_url: str | None = Field(default=None, max_length=2000)
    category: str = Field(min_length=1, max_length=120)
    type: str = Field(min_length=1, max_length=120)
    subtype: str = Field(min_length=1, max_length=120)

    @field_validator("name", "brand", "description", "category", "type", "subtype")
    @classmethod
    def nonempty(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Value cannot be blank")
        return clean

    @field_validator("image_url")
    @classmethod
    def require_https(cls, v: str | None) -> str | None:
        if not v or not v.strip():
            return None
        from urllib.parse import urlsplit
        parsed = urlsplit(v)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Image URL must be an HTTPS URL without credentials")
        return v


class ProductCreate(ProductFields):
    pass


class ProductUpdate(ProductFields):
    pass


class ProductPublic(ProductFields):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

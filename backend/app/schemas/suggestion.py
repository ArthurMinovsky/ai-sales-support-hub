from pydantic import BaseModel, Field, field_validator
from app.schemas.product import ProductPublic


class SuggestionRequest(BaseModel):
    query: str = Field(min_length=3, max_length=1500)

    @field_validator("query")
    @classmethod
    def nonempty_query(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise ValueError("Enter at least three characters")
        return cleaned


class SuggestedProduct(BaseModel):
    product_id: int
    product: ProductPublic
    reason: str


class SuggestionResponse(BaseModel):
    suggestions: list[SuggestedProduct]
    notice: str | None = None

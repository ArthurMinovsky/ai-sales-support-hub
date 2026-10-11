import re
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Product
from app.schemas.product import ProductPublic
from app.schemas.suggestion import SuggestedProduct, SuggestionResponse
from app.services.openrouter import request_ranking


def shortlist(query: str, products: list[Product], limit: int = 20) -> list[Product]:
    tokens = set(re.findall(r"\w+", query.lower(), flags=re.UNICODE))
    def score(p: Product) -> int:
        haystack = f"{p.name} {p.description} {p.category} {p.brand} {p.type} {p.subtype}".lower()
        return sum(1 for token in tokens if token in haystack)
    ranked = sorted(products, key=lambda p: (-score(p), p.id))
    return ranked[:limit]


async def suggest(query: str, db: Session) -> SuggestionResponse:
    products = list(db.scalars(select(Product).order_by(Product.id)).all())
    if not products:
        return SuggestionResponse(suggestions=[], notice="No products in the catalog yet. Add a product first.")
    candidates = shortlist(query, products)
    by_id = {p.id: p for p in candidates}
    raw = await request_ranking(query, [
        {"id": p.id, "name": p.name, "brand": p.brand, "description": p.description, "category": p.category, "type": p.type, "subtype": p.subtype}
        for p in candidates
    ])
    seen: set[int] = set()
    accepted = []
    for item in raw:
        product_id = item.get("product_id")
        reason = item.get("reason", "").strip()
        if product_id in by_id and product_id not in seen and reason:
            seen.add(product_id)
            accepted.append(SuggestedProduct(product_id=product_id, product=ProductPublic.model_validate(by_id[product_id]), reason=reason[:400]))
        if len(accepted) == 3:
            break
    return SuggestionResponse(suggestions=accepted, notice=None if accepted else "AI returned no matching catalog products.")

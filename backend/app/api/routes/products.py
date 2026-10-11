from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.models import Product, User
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductPublic, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["Products"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[ProductPublic])
def list_products(search: str | None = Query(default=None, max_length=180), db: Session = Depends(get_db)):
    query = select(Product).order_by(Product.id.desc())
    if search:
        pattern = f"%{search.strip()}%"
        query = query.where(or_(Product.name.ilike(pattern), Product.description.ilike(pattern), Product.category.ilike(pattern), Product.brand.ilike(pattern)))
    return db.scalars(query).all()


@router.post("", response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductPublic)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductPublic)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in payload.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return Response(status_code=204)

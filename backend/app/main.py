from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.session import get_engine, init_db
from app.seed import seed_demo_catalog
from app.api.routes import auth, products, suggestions


@asynccontextmanager
async def lifespan(app: FastAPI):
    if len(get_settings().jwt_secret) < 32:
        raise RuntimeError("Provide a strong JWT_SECRET (32+ characters) before starting the API")
    init_db()
    with Session(get_engine()) as session:
        seed_demo_catalog(session)
    yield


app = FastAPI(title="AI Sales Support Hub", version="1.0.0", lifespan=lifespan, description="Demo catalog and OpenRouter-grounded product suggestions")
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(suggestions.router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}

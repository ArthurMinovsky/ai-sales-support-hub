from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.security import start_new_session_epoch
from app.db.session import get_engine, init_db
from app.seed import seed_demo_catalog
from app.api.routes import auth, products, suggestions


@asynccontextmanager
async def lifespan(app: FastAPI):
    if len(get_settings().jwt_secret) < 32:
        raise RuntimeError("Provide a strong JWT_SECRET (32+ characters) before starting the API")
    start_new_session_epoch()
    init_db()
    with Session(get_engine()) as session:
        seed_demo_catalog(session)
    yield


app = FastAPI(title="AI Sales Support Hub", version="1.0.0", lifespan=lifespan, description="Demo catalog and OpenRouter-grounded product suggestions")


@app.exception_handler(RequestValidationError)
async def validation_error(request, exc: RequestValidationError):
    # Pydantic input/context may contain passwords or provider credentials.
    return JSONResponse(status_code=422, content={"detail": [
        {"type": error["type"], "loc": error["loc"], "msg": error["msg"]}
        for error in exc.errors()
    ]})


app.include_router(auth.router)
app.include_router(products.router)
app.include_router(suggestions.router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}

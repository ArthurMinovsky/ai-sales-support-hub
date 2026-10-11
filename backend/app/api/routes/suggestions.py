from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.suggestion import SuggestionRequest, SuggestionResponse
from app.services.recommendation import suggest
from app.services.openrouter import ProviderUnavailable

router = APIRouter(prefix="/api/suggestions", tags=["Suggestions"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=SuggestionResponse, responses={503: {"description": "AI_UNAVAILABLE — provider error"}})
async def recommendations(payload: SuggestionRequest, db: Session = Depends(get_db)):
    try:
        return await suggest(payload.query.strip(), db)
    except ProviderUnavailable:
        return JSONResponse(status_code=503, content={"code": "AI_UNAVAILABLE", "message": "AI recommendations are currently unavailable. Try again later."})

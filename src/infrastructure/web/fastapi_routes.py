from fastapi import HTTPException, Depends, APIRouter
from pydantic import BaseModel
from src.application.services import UrlShortenerService

class ShortenRequest(BaseModel):
    url: str

class ShortenResponse(BaseModel):
    short_code: str
    original_url: str

def get_url_shortener_service() -> UrlShortenerService:
    raise NotImplementedError("Esta dependencia debe ser inyectada en main.py")

router = APIRouter()

@router.post("/shorten", response_model=ShortenResponse)
def shorten_url(
    request: ShortenRequest,
    service: UrlShortenerService = Depends(get_url_shortener_service) 
):
    try:
        url_domain = service.shorten_url(request.url)

        return ShortenResponse(
            short_code=url_domain.short_code,
            original_url=url_domain.original_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{short_code}")
def redirect_url(
    short_code: str,
    service: UrlShortenerService = Depends(get_url_shortener_service)
):
    try:
        original_url = service.get_original_url(short_code)
        return {"url": original_url}
    except ValueError:
        raise HTTPException(status_code=404, detail="URL no encontrada")
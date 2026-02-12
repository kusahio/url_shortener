import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.sqlalchemy_repository import Base, SqlAlchemyUrlRepository
from src.infrastructure.web.fastapi_routes import router, get_url_shortener_service
from src.application.services import UrlShortenerService

DATABASE_URL = 'sqlite:///./database.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Url Shortener')

def get_db_session():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


def get_service_implementation(db_session = Depends(get_db_session)) -> UrlShortenerService:
  repository = SqlAlchemyUrlRepository(db_session)

  service = UrlShortenerService(repository)

  return service

app.dependency_overrides[get_url_shortener_service] = get_service_implementation

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
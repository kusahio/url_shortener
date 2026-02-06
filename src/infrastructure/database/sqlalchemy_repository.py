from typing import Optional
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, Session
from src.domain.url import Url
from src.application.ports import UrlRepository

Base = declarative_base()

class UrlModel(Base):
  __tablename__ = 'urls'

  id= Column(Integer, primary_key=True, index=True, autoincrement=True)
  original_url = Column(String, nullable=False)
  short_code = Column(String, unique=True, index=True, nullable=False)
  created_at = Column(DateTime, nullable=False)

class SqlAlchemyUrlRepository:
  def __init__(self, session: Session):
    self.session = session

  def save(self, url: Url) -> None:
    url_db_model = UrlModel(
          original_url=url.original_url,
          short_code=url.short_code,
          created_at=url.created_at
          # Nota: No pasamos 'id' porque la DB lo genera automáticamente
      )

    self.session.add(url_db_model)
    self.session.commit()
    self.session.refresh(url_db_model)

    if url.id is None:
      url.id = url_db_model.id
    
  def get_by_code(self, code: str) -> Optional[Url]:
    url_db_model = self.session.query(UrlModel).filter_by(short_code=code).first()

    if url_db_model:
      return Url(
        id=url_db_model.id,
        original_url=url_db_model.original_url,
        short_code=url_db_model.short_code,
        created_at=url_db_model.created_at
      )

    return None
from typing import Optional, Protocol
from src.domain.url import Url

class UrlRepository(Protocol):
  def save(self, url: Url) -> None:
    ...
  
  def get_by_code(self, code: str) -> Optional[Url]:
    ...
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import secrets
import string

@dataclass
class Url:
  original_url: str
  short_code: str
  created_at: datetime
  id: Optional[int] = None

  @staticmethod
  def create(original_url: str) -> Url:
    alphabet =  string.ascii_letters + string.digits
    code = "".join(secrets.choice(alphabet) for _ in range(6))

    return Url(
      original_url=original_url,
      short_code=code,
      created_at=datetime.now(),
      id=None
    )
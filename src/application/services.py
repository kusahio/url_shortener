from src.domain.url import Url
from src.application.ports import UrlRepository

class UrlShortenerService:
    def __init__(self, repository: UrlRepository):
        self.repository = repository

    def shorten_url(self, original_url: str) -> Url:
        new_url = Url.create(original_url)
        self.repository.save(new_url)

        return new_url

    def get_original_url(self, short_code: str) -> str:
        url = self.repository.get_by_code(short_code)

        if url is None:
            raise ValueError("URL not found")
            
        return url.original_url
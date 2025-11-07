import uuid

from core.domain.entities.news_article import NewsArticle
from core.domain.repositories.abstracts.abstract_new_repository import AbstractNewsRepository
from core.domain.repositories.abstracts.abstract_scraping_repository import (
    AbstractScrapingRepository,
)


class ExtractNewsContentUseCase:
    """Caso de uso para extrair conteúdo das notícias."""

    def __init__(
        self,
        scraping_repo: AbstractScrapingRepository,
        news_repo: AbstractNewsRepository,
    ):
        self._scraping_repo = scraping_repo
        self._news_repo = news_repo

    def execute(self, urls: list[str]) -> list[NewsArticle]:
        """Extrai conteúdo de uma lista de URLs."""
        articles = []

        for url in urls:
            content = self._scraping_repo.extract_content(url)
            article = NewsArticle(id=str(uuid.uuid4()), url=url, content=content)
            articles.append(article)
            self._news_repo.save(article)

        return articles


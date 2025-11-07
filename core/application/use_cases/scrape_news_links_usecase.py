from datetime import datetime, timedelta

from core.domain.repositories.abstracts.abstract_scraping_repository import (
    AbstractScrapingRepository,
)


class ScrapeNewsLinksUseCase:
    """Caso de uso para coletar links de notícias."""

    def __init__(self, scraping_repo: AbstractScrapingRepository):
        self._scraping_repo = scraping_repo

    def execute(self, base_url: str, days_ago: int = 1) -> list[str]:
        target_date = datetime.now() - timedelta(days=days_ago)
        return self._scraping_repo.scrape_news_links(base_url, target_date)

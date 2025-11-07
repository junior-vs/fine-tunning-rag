from abc import ABC, abstractmethod
from datetime import datetime


class AbstractScrapingRepository(ABC):
    """Repositório abstrato para operações de web scraping."""

    @abstractmethod
    def scrape_news_links(self, base_url: str, target_date: datetime) -> list[str]:
        """Extrai links de notícias de uma data específica."""
        pass

    @abstractmethod
    def extract_content(self, url: str) -> str:
        """Extrai conteúdo de um artigo específico."""
        pass

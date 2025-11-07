from abc import ABC, abstractmethod

from core.domain.entities.news_article import NewsArticle


class AbstractNewsRepository(ABC):
    """Repositório abstrato para artigos de notícia."""

    @abstractmethod
    def save(self, article: NewsArticle) -> None:
        """Salva um artigo."""
        pass

    @abstractmethod
    def find_by_id(self, article_id: str) -> NewsArticle | None:
        """Busca artigo por ID."""
        pass

    @abstractmethod
    def find_all(self) -> list[NewsArticle]:
        """Retorna todos os artigos."""
        pass

    @abstractmethod
    def save_batch(self, articles: list[NewsArticle]) -> None:
        """Salva múltiplos artigos."""
        pass

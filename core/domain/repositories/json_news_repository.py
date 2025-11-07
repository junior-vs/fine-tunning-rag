import json
import os
from typing import List, Optional

from core.domain.entities.news_article import NewsArticle
from core.domain.repositories.abstracts.abstract_new_repository import (
    AbstractNewsRepository,
)


class JSONNewsRepository(AbstractNewsRepository):
    """Implementação usando arquivo JSON."""

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._articles = self._load_articles()

    def _load_articles(self) -> dict:
        """Carrega artigos do arquivo JSON."""
        if os.path.exists(self._file_path):
            with open(self._file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_articles(self) -> None:
        """Salva artigos no arquivo JSON."""
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(self._articles, f, indent=4, ensure_ascii=False)

    def save(self, article: NewsArticle) -> None:
        """Salva um artigo."""
        self._articles[article.id] = {
            "id": article.id,
            "url": article.url,
            "title": article.title,
            "content": article.content,
            "summary": article.summary,
            "published_date": article.published_date.isoformat()
            if article.published_date
            else None,
            "source": article.source,
        }
        self._save_articles()

    def find_by_id(self, article_id: str) -> NewsArticle | None:
        """Busca artigo por ID."""
        data = self._articles.get(article_id)
        if not data:
            return None

        return NewsArticle(
            id=data["id"],
            url=data["url"],
            title=data.get("title"),
            content=data.get("content"),
            summary=data.get("summary"),
            source=data.get("source", "CNN"),
        )

    def find_all(self) -> list[NewsArticle]:
        """Retorna todos os artigos."""
        articles = []
        for data in self._articles.values():
            article = NewsArticle(
                id=data["id"],
                url=data["url"],
                title=data.get("title"),
                content=data.get("content"),
                summary=data.get("summary"),
                source=data.get("source", "CNN"),
            )
            articles.append(article)
        return articles

    def save_batch(self, articles: list[NewsArticle]) -> None:
        """Salva múltiplos artigos."""
        for article in articles:
            self.save(article)

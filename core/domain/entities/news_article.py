from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NewsArticle:
    """Entidade de domínio representando um artigo de notícia."""

    id: str
    url: str
    title: str | None = None
    content: str | None = None
    summary: str | None = None
    published_date: datetime | None = None
    source: str = "CNN"

    def __post_init__(self):
        if not self.url:
            raise ValueError("URL é obrigatória")
        if not self.id:
            raise ValueError("ID é obrigatório")

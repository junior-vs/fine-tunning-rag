from core.domain.entities.news_article import NewsArticle
from core.domain.repositories.abstracts.abstract_ai_repository import AbstractAIRepository
from core.domain.repositories.abstracts.abstract_new_repository import AbstractNewsRepository


class GenerateSummariesUseCase:
    """Caso de uso para gerar resumos das notícias."""

    def __init__(
        self, ai_repo: AbstractAIRepository, news_repo: AbstractNewsRepository
    ):
        self._ai_repo = ai_repo
        self._news_repo = news_repo

    def execute(self, articles: list[NewsArticle]) -> list[NewsArticle]:
        """Gera resumos para uma lista de artigos."""
        updated_articles = []

        for article in articles:
            if not article.content or len(article.content) < 150:
                continue

            summary = self._ai_repo.generate_summary(article.content)

            # Criar novo artigo com resumo (imutabilidade)
            updated_article = NewsArticle(
                id=article.id,
                url=article.url,
                title=article.title,
                content=article.content,
                summary=summary,
                published_date=article.published_date,
                source=article.source,
            )

            updated_articles.append(updated_article)
            self._news_repo.save(updated_article)

        return updated_articles

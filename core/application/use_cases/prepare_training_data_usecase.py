
from core.domain.entities.news_article import NewsArticle
from core.domain.entities.training_example import TrainingExample


class PrepareTrainingDataUseCase:
    """Caso de uso para preparar dados de treinamento."""

    def execute(self, articles: list[NewsArticle]) -> list[TrainingExample]:
        """Converte artigos em exemplos de treinamento."""
        training_examples = []

        """
        Para cada artigo, verifica se o conteúdo e o resumo não estão nulos e se o resumo não contém as palavras 'erro' ou 'insuficiente'.
        Apenas artigos válidos são convertidos em exemplos de treinamento.

        Returns:
            list[TrainingExample]: Lista de exemplos de treinamento gerados a partir dos artigos válidos.
        """
        for article in articles:
            if not article.content or not article.summary:
                continue

            if (
                "erro" in article.summary.lower()
                or "insuficiente" in article.summary.lower()
            ):
                continue

            try:
                example = TrainingExample.from_news_article(article)
                training_examples.append(example)
            except ValueError:
                continue

        return training_examples

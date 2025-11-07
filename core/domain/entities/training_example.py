from dataclasses import dataclass

from core.domain.entities.news_article import NewsArticle


@dataclass(frozen=True)
class TrainingExample:
    """Entidade representando um exemplo formatado para fine-tuning."""

    input_text: str

    @classmethod
    def from_news_article(cls, article: "NewsArticle") -> "TrainingExample":
        """Cria um exemplo de treinamento a partir de um artigo."""
        if not article.content or not article.summary:
            raise ValueError("Artigo deve ter conteúdo e resumo")

        formatted_text = (
            f"SUMMARIZE THIS NEWS.\n"
            f"[|News|] {article.content}[|eNews|]\n\n"
            f"[|summary|]{article.summary}[|esummary|]"
        )
        return cls(input_text=formatted_text)

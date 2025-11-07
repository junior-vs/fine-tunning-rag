from abc import ABC, abstractmethod


class AbstractAIRepository(ABC):
    """Repositório abstrato para operações de IA."""

    @abstractmethod
    def generate_summary(self, content: str) -> str:
        """Gera resumo para um conteúdo."""
        pass

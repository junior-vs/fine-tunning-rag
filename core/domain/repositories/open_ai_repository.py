import json

import openai
from openai import OpenAI

from core.domain.repositories.abstracts.abstract_ai_repository import (
    AbstractAIRepository,
)


class OpenAIRepository(AbstractAIRepository):
    """Implementação concreta usando OpenAI API."""

    def __init__(self, api_key: str):
        self._client = OpenAI(api_key=api_key)

    def generate_summary(self, content: str) -> str:
        """Gera resumo usando OpenAI."""
        try:
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": 'You are a JSON summarization bot. You MUST respond with ONLY a valid JSON object in the format {"summary": "your_summary_here"}.'
                    },
                    {"role": "user", "content": content}
                ],
                temperature=0.5,
                max_tokens=200
            )

            raw_response = response.choices[0].message.content

            if not raw_response:
                return "Erro: resposta vazia da API"

            try:
                summary_data = json.loads(raw_response)
                return summary_data.get("summary", "Erro ao extrair resumo")
            except json.JSONDecodeError:
                # Extração robusta de JSON
                start_index = raw_response.find('{')
                end_index = raw_response.rfind('}') + 1
                if start_index != -1 and end_index != 0:
                    clean_json = raw_response[start_index:end_index]
                    summary_data = json.loads(clean_json)
                    return summary_data.get("summary", "Erro ao extrair resumo")
                return "Erro no formato da resposta"

        except (openai.APIError, openai.AuthenticationError, openai.RateLimitError) as api_exc:
            return f"Erro na API: {str(api_exc)}"
        except Exception as exc:
            return f"Erro inesperado: {str(exc)}"


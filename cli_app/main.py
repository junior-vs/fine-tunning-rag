"""CLI application using Typer."""

import json
import os

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from core.application.use_cases.extract_news_content_usecase import (
    ExtractNewsContentUseCase,
)
from core.application.use_cases.generate_summaries_usecase import (
    GenerateSummariesUseCase,
)
from core.application.use_cases.prepare_training_data_usecase import (
    PrepareTrainingDataUseCase,
)
from core.application.use_cases.scrape_news_links_usecase import ScrapeNewsLinksUseCase
from core.domain.repositories.cnn_scraping_repository import CNNScrapingRepository
from core.domain.repositories.json_news_repository import JSONNewsRepository
from core.domain.repositories.open_ai_repository import OpenAIRepository

app = typer.Typer()
console = Console()


@app.command()
def run_pipeline(
    output_dir: str = typer.Option("./data", help="Diretório de saída"),
):
    """Executa o pipeline completo de preparação de dados."""

    # Buscar API key do arquivo .env
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        typer.echo(
            "❌ OPENAI_API_KEY não encontrada no arquivo .env.\n"
            "Por favor, crie um arquivo .env na raiz do projeto e adicione a linha:\n"
            "OPENAI_API_KEY=seu_api_key_aqui"
        )
        raise typer.Exit(1)

    # Configuração dos repositórios
    scraping_repo = CNNScrapingRepository()
    ai_repo = OpenAIRepository(openai_api_key)
    news_repo = JSONNewsRepository(os.path.join(output_dir, "articles.json"))

    # Casos de uso
    scrape_links_uc = ScrapeNewsLinksUseCase(scraping_repo)
    extract_content_uc = ExtractNewsContentUseCase(scraping_repo, news_repo)
    generate_summaries_uc = GenerateSummariesUseCase(ai_repo, news_repo)
    prepare_data_uc = PrepareTrainingDataUseCase()

    # Execução do pipeline
    typer.echo("🔗 Coletando links...")
    links = scrape_links_uc.execute("https://edition.cnn.com/world")
    typer.echo(f"Encontrados {len(links)} links")

    typer.echo("📰 Extraindo conteúdo...")
    articles = extract_content_uc.execute(links)
    typer.echo(f"Extraídos {len(articles)} artigos")

    typer.echo("🤖 Gerando resumos...")
    articles_with_summaries = generate_summaries_uc.execute(articles)
    typer.echo(f"Gerados {len(articles_with_summaries)} resumos")

    typer.echo("📚 Preparando dados de treinamento...")
    training_examples = prepare_data_uc.execute(articles_with_summaries)

    # Salvar dados finais
    output_file = os.path.join(output_dir, "training_data.json")
    training_data = [{"input": example.input_text} for example in training_examples]

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(training_data, f, indent=4, ensure_ascii=False)

    typer.echo(
        f"✅ Pipeline concluído! {len(training_examples)} exemplos salvos em {output_file}"
    )


if __name__ == "__main__":
    app()

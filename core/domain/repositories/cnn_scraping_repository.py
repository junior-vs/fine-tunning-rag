import json
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from core.domain.repositories.abstracts.abstract_scraping_repository import (
    AbstractScrapingRepository,
)


class CNNScrapingRepository(AbstractScrapingRepository):
    """Implementação concreta para scraping da CNN."""

    def __init__(self):
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def scrape_news_links(self, base_url: str, target_date: datetime) -> List[str]:
        """Implementa scraping de links da CNN."""
        try:
            response = requests.get(base_url, headers=self._headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            valid_links = []

            for a_tag in soup.find_all("a", href=True):
                href = str(a_tag["href"])

                # Filtro de vídeo
                if "/video/" in href:
                    continue

                # Verificação de data na URL
                path_parts = href.strip("/").split("/")
                if (
                    len(path_parts) >= 3
                    and path_parts[0].isdigit()
                    and len(path_parts[0]) == 4
                ):
                    try:
                        url_year = int(path_parts[0])
                        url_month = int(path_parts[1])
                        url_day = int(path_parts[2])

                        if (
                            url_year == target_date.year
                            and url_month == target_date.month
                            and url_day == target_date.day
                        ):
                            full_link = f"https://edition.cnn.com{href}"
                            valid_links.append(full_link)
                    except (ValueError, IndexError):
                        continue

            return sorted(set(valid_links))

        except requests.exceptions.RequestException as e:
            print(f"Error scraping news links from {base_url}: {e}")
            return []

    def extract_content(self, url: str) -> str:
        """Implementa extração de conteúdo da CNN."""
        try:
            response = requests.get(url, headers=self._headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Método preferencial: JSON-LD
            json_ld_scripts = soup.find_all("script", type="application/ld+json")
            for script in json_ld_scripts:
                try:
                    if script.string is None:
                        continue
                    data = json.loads(script.string)
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and "articleBody" in item:
                                return item["articleBody"]
                    elif isinstance(data, dict) and "articleBody" in data:
                        return data["articleBody"]
                except (json.JSONDecodeError, TypeError):
                    continue

            # Fallback: HTML scraping
            main_container = soup.find("div", class_="article__content-container")
            if not main_container:
                main_container = soup.find("div", class_="article__content")
            if main_container:
                paragraphs = main_container.find_all(
                    "div", {"data-component-name": "paragraph"}
                )
                if not paragraphs:
                    paragraphs = main_container.find_all("p", class_="paragraph")

                if paragraphs:
                    content = " ".join(p.get_text(strip=True) for p in paragraphs)
                    return content

            return "Conteúdo não encontrado"
        except requests.exceptions.RequestException as e:
            # Log the exception details for debugging
            print(f"Erro de rede ao acessar {url}: {e}")
            return f"Erro de rede: {e}"
            return "Erro de rede"

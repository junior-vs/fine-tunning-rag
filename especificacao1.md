Entendido. Com base em todas as suas orientações e nos ajustes na estrutura de diretórios, vou gerar a **Especificação Técnica Completa do Projeto** formatada para ser utilizada como o documento principal de detalhamento e como *input* para a LLM, garantindo a fidelidade ao DDD, SOLID e Clean Architecture.

-----

# 🚀 ESPECIFICAÇÃO TÉCNICA E ARQUITETURAL: PROJETO MODULARIZADO PYTHON

## 1\. Visão Geral e Fundamentos do Projeto

Este projeto define um *template* de aplicação Python com foco em **escalabilidade e manutenibilidade**, utilizando as metodologias mais avançadas para a separação da lógica de negócio.

| Item | Especificação |
| :--- | :--- |
| **Nome do Projeto** | `meu_projeto` (Pacote principal: `core`) |
| **Linguagem / Versão** | Python \>= 3.11 |
| **Arquitetura Principal** | Clean Architecture (Modelo em Cebola) |
| **Metodologia de Domínio** | Domain-Driven Design (DDD) |
| **Padrões de Código** | SOLID (Ênfase em S, O, D) e Programação Híbrida (OO/FP) |
| **Gerenciamento** | `uv` e `pyproject.toml` (PEP 621) |
| **Interfaces de Usuário** | API HTTP (FastAPI) e CLI (Typer) |

## 2\. Princípios de Design e Justificativas

As decisões arquiteturais são guiadas estritamente pelos seguintes princípios:

| Princípio Aplicado | Descrição e Justificativa |
| :--- | :--- |
| **Clean Architecture / DDD** | O módulo **`core`** é a camada de Domínio, Application e Infraestrutura. Ele é a camada mais interna e totalmente independente dos detalhes de entrega (HTTP, CLI). **Motivo:** Protege as regras de negócio de mudanças tecnológicas. |
| **Inversão de Dependência (D de SOLID)** | A camada `core/application` depende de **Abstrações** (`core/domain/repositories`) e não de implementações concretas (ex: `PostgresRepository` que está em `core/infrastructure`). **Motivo:** Permite que o *core* seja totalmente testado sem a necessidade de banco de dados ou frameworks. |
| **Separação de Responsabilidades (S de SOLID)** | Cada módulo (`core`, `cli_app`, `http_app`) tem uma única razão para mudar. **Motivo:** Interfaces diferentes não afetam o **`core`** e vice-versa. |
| **Programação Híbrida (OO/FP)** | **OO** para o **Domínio (`core/domain`)** (Entidades, Aggregates com estado e identidade). **FP** para **Serviços/Funções Puras** na camada de Aplicação. **Motivo:** Usa o melhor de cada paradigma: modelagem realista de objetos com OO e lógica de transformação previsível com FP. |

## 3\. Estrutura de Diretórios (Nível Raiz)

A estrutura é a seguinte. O LLM deve gerar o código **dentro** desses diretórios, começando pelo nível do `pyproject.toml`.

```
.
├── core/
│   ├── __init__.py           # Marca 'core' como um pacote Python
│   ├── domain/               # 💡 CAMADA 1: Entidades, VOs e Abstrações (Portas)
│   │   ├── entities/         # Classes de Domínio (OO, com identidade)
│   │   │   └── item.py       # Exemplo de Entidade
│   │   └── repositories/     # Classes Abstratas para Inversão de Dependência (D de SOLID)
│   │       └── item_repo.py  # Exemplo: AbstractItemRepository(ABC)
│   ├── application/          # 💡 CAMADA 2: Casos de Uso
│   │   └── use_cases/        # Classes de Use Cases (orquestração)
│   │       └── create_item_uc.py # Exemplo: Recebe o AbstractRepo, usa a Entidade.
│   └── infrastructure/       # 💡 CAMADA 4: Implementações de Repositório (Adaptadores Concretos)
│       └── repositories/     # Exemplo: InMemoryItemRepository(AbstractItemRepository)
├── cli_app/                  # 💡 CAMADA 3: Adaptador de Entrega (CLI)
│   └── main.py               # Ponto de entrada, injeta infraestrutura real no Use Case
├── http_app/                 # 💡 CAMADA 3: Adaptador de Entrega (HTTP/API)
│   └── main.py               # Configura FastAPI, injeta infraestrutura real no Use Case
├── tests/                    # Diretório de Testes (Deve espelhar a estrutura do código)
│   ├── core/
│   ├── cli_app/
│   └── http_app/
├── pyproject.toml            # Configuração unificada do projeto
├── uv.lock                   # Gerado pelo 'uv'
└── README.md
```

## 4\. Conteúdo Mínimo de Arquivos (Protótipos)

O LLM deve gerar o conteúdo inicial dos seguintes arquivos para demonstrar a aplicação da arquitetura:

### A. `core/domain/repositories/item_repo.py`

  * **Conteúdo:** Definição de `AbstractItemRepository` usando `abc.ABC`.
  * **Propósito:** Fornecer a **interface (porta)** que o `CreateItemUseCase` dependerá.

### B. `core/domain/entities/item.py`

  * **Conteúdo:** Definição de uma classe `Item` usando **`dataclasses`** ou **`pydantic`** (para imutabilidade se possível) com atributos básicos (ID, nome).
  * **Propósito:** Definir o objeto de domínio central.

### C. `core/application/use_cases/create_item_uc.py`

  * **Conteúdo:** Classe `CreateItemUseCase` que recebe o `AbstractItemRepository` no construtor.
  * **Propósito:** Demonstrar a **Inversão de Dependência** e a lógica de orquestração (`repo.save(item)`).

### D. `http_app/main.py`

  * **Conteúdo:** Configuração básica do **FastAPI**.
  * **Endpoint:** Criar uma rota POST `/items` que:
    1.  Instancia a implementação concreta do repositório (`InMemoryItemRepository` de `core/infrastructure`).
    2.  Instancia o `CreateItemUseCase`, injetando a implementação concreta.
    3.  Chama o método `execute()` do Use Case.
  * **Propósito:** Demonstrar a função da camada Adaptadora: **conectar a infraestrutura real com a lógica de aplicação**.

### E. `tests/core/test_use_cases.py`

  * **Conteúdo:** Um teste unitário simples para `CreateItemUseCase` usando o *Mock* do Python para simular a dependência (`AbstractItemRepository`).
  * **Propósito:** Validar que o Use Case pode ser testado isoladamente.

### F. `pyproject.toml`

  * **Conteúdo:** Configuração completa conforme detalhado na Seção 2 da especificação anterior.

## 5\. Ferramentas e Configuração Inicial

O projeto deve incluir os comandos iniciais no `README.md` e a configuração no `pyproject.toml` para as ferramentas de qualidade:

  * **`ruff`:** Configurado para **Linting e Formatação** com `line-length = 88`.
  * **`mypy`:** Configurado para checagem de tipos na pasta `core/`.
  * **`pytest`:** Comando de execução configurado para rodar a partir do ambiente `uv run pytest`.
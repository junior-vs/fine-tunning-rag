# 🚀 Meu Projeto - Clean Architecture + DDD + SOLID

Projeto Python modularizado seguindo **Clean Architecture**, **Domain-Driven Design (DDD)** e princípios **SOLID**.

## 📁 Estrutura do Projeto

```
.
├── core/                          # 💡 Camadas: Domain, Application, Infrastructure
│   ├── domain/                    # Entidades, Value Objects e Portas (Interfaces)
│   │   ├── entities/              # Entidades de Domínio (OO)
│   │   └── repositories/          # Interfaces de Repositório (Inversão de Dependência)
│   ├── application/               # Casos de Uso (Orquestração)
│   │   └── use_cases/
│   └── infrastructure/            # Implementações Concretas (Adaptadores)
│       └── repositories/
├── cli_app/                       # 💡 Interface CLI (Typer)
│   └── main.py
├── http_app/                      # 💡 Interface HTTP/API (FastAPI)
│   └── main.py
├── tests/                         # Testes Unitários
└── pyproject.toml                 # Configuração do Projeto
```

## 🎯 Princípios Arquiteturais

- **Clean Architecture**: Separação em camadas (Domain → Application → Infrastructure → Interfaces)
- **DDD**: Entidades, Value Objects, Repositórios
- **SOLID**: Inversão de Dependência, Responsabilidade Única
- **Programação Híbrida**: OO para Domínio, FP para Casos de Uso

## 🛠️ Instalação

### Pré-requisitos
- Python >= 3.11
- uv (gerenciador de pacotes)

### Configuração

```bash
# Instalar dependências
uv sync

# Instalar dependências de desenvolvimento
uv sync --extra dev
```

## 🚀 Execução

### API HTTP (FastAPI)

```bash
# Iniciar servidor
uv run uvicorn http_app.main:app --reload

# Acessar documentação interativa
# http://localhost:8000/docs
```

### CLI (Typer)

```bash
# Criar um item
uv run python -m cli_app.main create "Nome do Item" --description "Descrição"

# Listar itens
uv run python -m cli_app.main list
```

## 🧪 Testes

```bash
# Executar todos os testes
uv run pytest

# Executar com cobertura
uv run pytest --cov=core --cov-report=html

# Executar testes específicos
uv run pytest tests/core/test_use_cases.py
```

## 🔍 Qualidade de Código

### Linting e Formatação (Ruff)

```bash
# Verificar código
uv run ruff check .

# Formatar código
uv run ruff format .

# Corrigir problemas automaticamente
uv run ruff check --fix .
```

### Checagem de Tipos (MyPy)

```bash
# Verificar tipos
uv run mypy core/
```

## 📝 Exemplo de Uso

### API HTTP

```bash
# Criar item
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "Notebook", "description": "Dell XPS 15"}'

# Listar itens
curl "http://localhost:8000/items"

# Obter item específico
curl "http://localhost:8000/items/{item_id}"

# Deletar item
curl -X DELETE "http://localhost:8000/items/{item_id}"
```

### CLI

```bash
# Criar item
uv run python -m cli_app.main create "Notebook" -d "Dell XPS 15"

# Listar todos os itens
uv run python -m cli_app.main list
```

## 🏗️ Arquitetura

### Camada de Domínio (core/domain)
- **Entidades**: Objetos com identidade (`Item`)
- **Repositórios**: Interfaces abstratas (Portas)

### Camada de Aplicação (core/application)
- **Casos de Uso**: Orquestração da lógica de negócio
- **Inversão de Dependência**: Depende de abstrações, não de implementações

### Camada de Infraestrutura (core/infrastructure)
- **Repositórios Concretos**: Implementações (In-Memory, PostgreSQL, etc.)
- **Adaptadores**: Conectam o domínio com tecnologias externas

### Camada de Interface (cli_app, http_app)
- **HTTP API**: FastAPI endpoints
- **CLI**: Comandos Typer
- **Injeção de Dependência**: Instancia implementações concretas

## 📚 Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **Typer**: Framework CLI com suporte a rich formatting
- **Pydantic**: Validação de dados
- **Pytest**: Framework de testes
- **Ruff**: Linter e formatador ultra-rápido
- **MyPy**: Checagem estática de tipos
- **UV**: Gerenciador de pacotes Python moderno

## 🤝 Contribuindo

1. Siga os princípios SOLID e Clean Architecture
2. Mantenha a cobertura de testes acima de 80%
3. Execute linting e type checking antes de commitar
4. Documente casos de uso complexos
fine tunning &amp; rag

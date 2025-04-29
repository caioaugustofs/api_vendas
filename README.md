# API Vendas

API para gerenciamento de produtos, estoque, fornecedores e usuários.

## Funcionalidades
- Cadastro, listagem, atualização e remoção de produtos
- Controle de estoque (entrada, saída, consulta)
- Cadastro e gerenciamento de fornecedores
- Cadastro e gerenciamento de usuários

## Endpoints principais
- `/produtos/` — CRUD de produtos
- `/estoque/` — Controle de estoque
- `/fornecedores/` — CRUD de fornecedores
- `/users/` — CRUD de usuários

## Tecnologias
- Python 3.13
- FastAPI
- SQLAlchemy (async)
- Alembic (migrations)
- SQLite (padrão, pode ser trocado por outro)
- Poetry (gerenciador de dependências)

## Como rodar o projeto

1. Instale as dependências:
   ```bash
   poetry install
   ```
2. Configure o arquivo `.env` com a string de conexão do banco de dados.
3. Execute as migrations:
   ```bash
   alembic upgrade head
   ```
4. Rode a aplicação:
   ```bash
   poetry run fastapi dev vender_api/app.py --port 8001
   ```

## Estrutura de pastas
- `vender_api/` — Código principal da API
- `migrations/` — Migrations do banco de dados
- `tests/` — Testes automatizados

## Contribuição
Pull requests são bem-vindos!

---

> Projeto desenvolvido por Caio Augusto e colaboradores.

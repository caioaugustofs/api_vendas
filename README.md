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

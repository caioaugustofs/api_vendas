from fastapi import FastAPI

from vender_api.routers.v1 import (
    auth,
    categorias_routers,
    estoque_routers,
    fornecedores_routers,
    movimentacao_estoque_routers,
    produtos_routers,
    users_root_routers,
    users_routers,
)

app = FastAPI(
    title='API de Vendas',
    description=('API de Vendas é uma API RESTful desenvolvida com FastAPI, '),
    version='0.1.0',
)


app.include_router(produtos_routers.router)
app.include_router(estoque_routers.router)
app.include_router(movimentacao_estoque_routers.router)
app.include_router(fornecedores_routers.router)
app.include_router(categorias_routers.router)
app.include_router(users_routers.router)
app.include_router(users_root_routers.router)
app.include_router(auth.router)

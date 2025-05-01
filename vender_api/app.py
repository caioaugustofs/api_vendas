from fastapi import FastAPI

from vender_api.routers.v1 import (
    auth,
    estoque_routers,
    produtos_routers,
    users_root_routers,
    users_routers,
)

app = FastAPI(
    title='API de Vendas',
    description=('API de Vendas é uma API RESTful desenvolvida com FastAPI, '),
    version='X.1.0',
)

app.include_router(produtos_routers.router)
app.include_router(estoque_routers.router)
app.include_router(users_routers.router)
app.include_router(users_root_routers.router)
app.include_router(auth.router)

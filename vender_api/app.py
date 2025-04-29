from fastapi import FastAPI

from vender_api.routers.v1 import (
    categorias_routers,
    estoque_routers,
    fornecedores_routers,
    produtos_routers,
    users_routers,
)

app = FastAPI()


app.include_router(categorias_routers.router)
app.include_router(produtos_routers.router)
app.include_router(estoque_routers.router)
app.include_router(fornecedores_routers.router)
app.include_router(users_routers.router)
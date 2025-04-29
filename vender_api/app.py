from fastapi import FastAPI

from vender_api.routers.v1 import estoque_routers, produtos_routers

app = FastAPI()


app.include_router(produtos_routers.router)
app.include_router(estoque_routers.router)

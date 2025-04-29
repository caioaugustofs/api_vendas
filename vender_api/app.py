from fastapi import FastAPI

from vender_api.routers.v1 import produtos_routers

app = FastAPI()


app.include_router(produtos_routers.router)

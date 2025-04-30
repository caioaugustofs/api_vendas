from fastapi import FastAPI

from vender_api.routers.v1 import (
    auth,
    users_root_routers,
    users_routers,
)

app = FastAPI()


app.include_router(users_routers.router)
app.include_router(users_root_routers.router)
app.include_router(auth.router)

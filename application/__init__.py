from fastapi import FastAPI
from .config import get_config
from fastapi.middleware.cors import CORSMiddleware
from .shared.databases import async_db


app = FastAPI(
    title=get_config().app_name,
    version=get_config().app_version,
    description="The 11SevenPortfolio API.",
    docs_url=None,
    redoc_url="/",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await async_db().connect()


@app.on_event("shutdown")
async def shutdown():
    await async_db().disconnect()


__all__ = ["app"]

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.infrastructure.fastapi.middlewares import ProcessTimeHeaderMiddleware
from src.ui.rest.router import router as rest_router


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    logging.info("Starting FastAPI application")

    try:
        yield
    finally:
        logging.info("Shutting down FastAPI application")


def create_app() -> FastAPI:
    app_title = "Lesta Games Test Task"
    app_version = "0.1.0"
    app_description = "API for Lesta Games Test Task"
    app_ = FastAPI(
        title=app_title,
        version=app_version,
        description=app_description,
        lifespan=lifespan,
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[],
    )

    app_.add_middleware(
        ProcessTimeHeaderMiddleware,
        service_name='Auth'
    )

    app_.include_router(rest_router)

    return app_

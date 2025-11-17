import asyncio
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from ml_backend.utils.reconciler import reconciler_loop


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(reconciler_loop())
    yield
    task.cancel()


def create_app(router: APIRouter):
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    return app

import uvicorn

from ml_backend.api.router import router
from ml_backend.app import create_app


def main() -> None:
    app = create_app(router)

    uvicorn.run(app, host="0.0.0.0")

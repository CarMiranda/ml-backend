from typing import Any

from pydantic import BaseModel


class JobSubmitRequest(BaseModel):
    entrypoint: str
    runtime_env: dict[str, Any]
    webhook_url: str | None = None
    params: dict[str, Any] = {}


class JobResponse(BaseModel):
    job_id: str
    ray_job_id: str
    status: str

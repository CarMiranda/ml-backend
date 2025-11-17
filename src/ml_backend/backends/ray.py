import httpx

from ml_backend.settings import settings


def submit_job(entrypoint: str, runtime_env: dict):
    url = f"{settings.RAY_HEAD_URL}/api/jobs/"
    payload = {"entrypoint": entrypoint, "runtime_env": runtime_env}
    r = httpx.post(url, json=payload)
    r.raise_for_status()
    return r.json()["job_id"]


def get_status(ray_job_id: str):
    url = f"{settings.RAY_HEAD_URL}/api/jobs/{ray_job_id}"
    r = httpx.get(url)
    r.raise_for_status()
    data = r.json()
    return data.get("status"), data.get("message")


def cancel_job(ray_job_id: str):
    url = f"{settings.RAY_HEAD_URL}/api/jobs/{ray_job_id}"
    r = httpx.delete(url)
    r.raise_for_status()
    data = r.json()
    return data.get("status"), data.get("message")

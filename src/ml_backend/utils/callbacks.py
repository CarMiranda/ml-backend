import requests

from ml_backend.settings import settings


def send_webhook(url: str, payload: dict):
    try:
        requests.post(url, json=payload, timeout=settings.WEBHOOK_TIMEOUT)
    except Exception:
        # TODO: Retry, and store retries log in db ?
        pass

import asyncio

from sqlalchemy.orm import Session

from ml_backend.backends.ray import get_status
from ml_backend.database import SessionLocal
from ml_backend.models import Job
from ml_backend.settings import settings
from ml_backend.utils.callbacks import send_webhook


async def reconciler_loop():
    while True:
        await asyncio.sleep(settings.RECONCILE_INTERVAL)
        try:
            db: Session = SessionLocal()
            jobs = db.query(Job).filter(Job.status.in_(["QUEUED", "RUNNING"])).all()

            for job in jobs:
                if not job.ray_job_id:
                    continue

                status, msg = get_status(job.ray_job_id)
                if status != job.status:
                    job.status = status
                    db.commit()

                    if job.webhook_url:
                        send_webhook(
                            job.webhook_url,
                            {"job_id": job.id, "status": job.status, "message": msg},
                        )

        except Exception as e:
            print("[Reconciler] Error:", e)

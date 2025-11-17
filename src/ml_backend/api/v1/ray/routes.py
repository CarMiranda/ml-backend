import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ml_backend.api.common import get_db
from ml_backend.backends.ray import cancel_job
from ml_backend.backends.ray import submit_job as submit_ray_job
from ml_backend.models import Job
from ml_backend.schemas import JobResponse, JobSubmitRequest

router = APIRouter(tags=["ray"])


@router.post("/jobs", response_model=JobResponse, status_code=202)
def submit_job(req: JobSubmitRequest, db: Session = Depends(get_db)):
    job_id = str(uuid.uuid4())
    ray_job_id = submit_ray_job(req.entrypoint, req.runtime_env)

    job = Job(
        id=job_id,
        ray_job_id=ray_job_id,
        status="QUEUED",
        config=req.params,
        webhook_url=req.webhook_url,
    )
    db.add(job)
    db.commit()

    return JobResponse(job_id=job_id, ray_job_id=ray_job_id, status="QUEUED")


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.scalars(select(Job).where(Job.id == job_id)).one()
    if not job:
        return {"error": "not found"}
    return JobResponse(job_id=job.id, ray_job_id=job.ray_job_id, status=job.status)


@router.delete("/jobs/{job_id}", response_model=JobResponse)
def delete_job(job_id: str, db: Session = Depends(get_db)):
    job = db.scalars(select(Job).where(Job.id == job_id)).one()
    if not job:
        return {"error": "not found"}

    status, _ = cancel_job(job.ray_job_id)
    if 200 < status or status >= 300:
        return {"error": "not found"}

    job.status = "CANCELLED"
    db.commit()

    return JobResponse(job_id=job.id, ray_job_id=job.ray_job_id, status=job.status)

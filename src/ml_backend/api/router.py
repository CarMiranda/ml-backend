from fastapi import APIRouter

from ml_backend.api.v1.ray.routes import router as ray_router

router = APIRouter()
router.include_router(ray_router)

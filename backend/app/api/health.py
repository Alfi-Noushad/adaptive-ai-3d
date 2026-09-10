from fastapi import APIRouter
from app.schemas.response import APIResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=APIResponse)
async def health_check():
    return APIResponse(
        status="ok",
        message="Backend service is operational",
        data={"service": "2d-to-3d-converter-backend"}
    )
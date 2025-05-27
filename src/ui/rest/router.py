from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.utils.exceptions import http_exc

from .texts_analysis.router import router as texts_analysis_router


router = APIRouter(
    prefix="/api/v1",
    responses={
        **http_exc.NotFoundHTTPException.docs()
    }
)


router.include_router(texts_analysis_router)


@router.get(
    "/healthcheck",
    responses={
        200: {
            "description": "API is healthy",
            "content": {"application/json": {"example": {"status": "ok", "message": "API is healthy"}}}
        }
    },
)
async def healthcheck() -> JSONResponse:
    """
    Healthcheck endpoint to verify the API is running.
    """
    return JSONResponse({"status": "ok", "message": "API is healthy"}, status_code=200)

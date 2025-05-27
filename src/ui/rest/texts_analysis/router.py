from fastapi import APIRouter


from .tf_idf import router as tf_idf_router


router = APIRouter(
    prefix="/text-analysis",
    tags=["Text Analysis"],
)

router.include_router(tf_idf_router)



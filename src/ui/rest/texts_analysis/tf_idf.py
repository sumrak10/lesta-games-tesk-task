from typing import Literal

from fastapi import APIRouter, UploadFile, File

from src.application.transport.text_analysis.tf_idf import TfidfAnalysisResultDTO
from src.application.use_cases.text_analysis.tf_idf import TextAnalysisTfidfUseCase
from src.utils.exceptions import http_exc

router = APIRouter(
    prefix="/tf-idf",
)


@router.post(
    "/",
    summary="Calculate TF-IDF",
    description="Calculate the Term Frequency-Inverse Document Frequency (TF-IDF) for a given text.",
    responses={
        **http_exc.BadRequestHTTPException.docs()
    }
)
async def calculate_tf_idf(
    files: list[UploadFile] = File(...),
    order_by: Literal['tf_score', 'idf_score', 'tf_idf_score'] | None = 'idf_score',
    order_by_asc: bool = False
) -> list[TfidfAnalysisResultDTO]:
    return await TextAnalysisTfidfUseCase.analyse(
        files,
        order_by=order_by,
        order_by_asc=order_by_asc
    )

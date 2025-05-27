from fastapi import UploadFile

from src.application.transport.text_analysis.tf_idf import TfidfInputDTO, TfidfAnalysisResultDTO, TfidfWordAnalysisDTO
from src.domain.services.text_analysis.tf_idf import TextAnalysisTfidfService
from src.utils.exceptions import http_exc


class TextAnalysisTfidfUseCase:
    @classmethod
    async def analyse(
        cls,
        files: list[UploadFile],
        *,
        order_by: str | None,
        order_by_asc: bool,
    ) -> list[TfidfAnalysisResultDTO]:
        """
        Analyzes the given texts using TF-IDF vectorization.
        :param files: List of uploaded files containing texts to analyze.
        :param order_by: Optional parameter to specify sorting criteria.
        :param order_by_asc: Boolean indicating whether to sort in ascending order.
        :return: List if TfidfAnalysisResultDTO containing the analysis results.
        """
        if any(file.content_type != 'text/plain' for file in files):
            raise http_exc.BadRequestHTTPException("All files must be plain text files (text/plain).")

        input_dtos = [
            TfidfInputDTO(
                file_name=file.filename,
                text=(await file.read()).decode('utf-8')
            )
            for file in files
        ]

        try:
            results = await TextAnalysisTfidfService.analyse(input_dtos, stop_words=None)
        except ValueError as e:
            raise http_exc.BadRequestHTTPException(f"Empty vocabulary; perhaps the documents only contain stop words")

        for result in results:
            if order_by is not None:
                try:
                    result.words.sort(key=lambda x: getattr(x, order_by), reverse=not order_by_asc)
                except AttributeError:
                    raise http_exc.BadRequestHTTPException(
                        f"Invalid order_by field: {order_by}. "
                        f"Must be a valid value of {TfidfWordAnalysisDTO.model_fields.keys()}."
                    )

        return results

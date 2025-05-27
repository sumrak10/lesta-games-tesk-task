from pydantic import BaseModel


class TfidfInputDTO(BaseModel):
    file_name: str
    text: str


class TfidfWordAnalysisDTO(BaseModel):
    word: str
    tf_score: float
    idf_score: float
    tf_idf_score: float


class TfidfAnalysisResultDTO(BaseModel):
    file_name: str
    words: list[TfidfWordAnalysisDTO]

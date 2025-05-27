import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from src.application.transport.text_analysis.tf_idf import TfidfInputDTO, TfidfAnalysisResultDTO, TfidfWordAnalysisDTO
from src.config.text_analysis import text_analysis_settings


class TextAnalysisTfidfService:
    @classmethod
    async def analyse(
        cls,
        input_dtos: list[TfidfInputDTO],
        *,
        stop_words: set[str] | None = None,
    ) -> list[TfidfAnalysisResultDTO]:
        """
        Analyzes the given texts using TF-IDF vectorization.
        :param input_dtos: List of input DTOs containing file names and texts to analyze.
        :param stop_words: List of stop words to ignore during analysis. If None, default stop words will be used.
        :return:
        """
        if not input_dtos:
            return []

        texts = [dto.text for dto in input_dtos]
        vectorizer = TfidfVectorizer(stop_words=stop_words or list(text_analysis_settings.RUSSIAN_STOP_WORDS))
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        idf_scores = vectorizer.idf_.tolist()

        dense = tfidf_matrix.todense()
        arr = np.asarray(dense)

        results: list[TfidfAnalysisResultDTO] = []
        for doc_idx, dto in enumerate(input_dtos):
            words_analysis: list[TfidfWordAnalysisDTO] = []
            for feat_idx, word in enumerate(feature_names):
                tf = float(arr[doc_idx, feat_idx])
                idf = float(idf_scores[feat_idx])
                if tf == 0:
                    continue
                words_analysis.append(
                    TfidfWordAnalysisDTO(
                        word=word,
                        tf_score=tf,
                        idf_score=idf,
                        tf_idf_score=tf * idf,
                    )
                )
            results.append(TfidfAnalysisResultDTO(file_name=dto.file_name, words=words_analysis))

        return results



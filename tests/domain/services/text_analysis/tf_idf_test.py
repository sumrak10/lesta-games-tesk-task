import pytest
import numpy as np
from pydantic import ValidationError

from src.application.transport.text_analysis.tf_idf import (
    TfidfInputDTO,
    TfidfWordAnalysisDTO,
    TfidfAnalysisResultDTO,
)
from src.domain.services.text_analysis.tf_idf import TextAnalysisTfidfService
import src.domain.services.text_analysis.tf_idf as tfidf_module


class DummyVectorizer:
    def __init__(self, stop_words):
        self.stop_words = stop_words

        # idf_ values for our tests
        class IdfDummy:
            def __init__(self, items):
                self._items = items

            def tolist(self):
                return self._items

        self.idf_ = IdfDummy([1.0, 2.0, 3.0])

    def fit_transform(self, texts):
        # Simulate a TF-IDF matrix with multiple rows of three term scores
        class DummyMatrix:
            def __init__(self, data):
                self._data = data

            def todense(self):
                return np.array(self._data)

        # For each text, return same tf scores [0.1, 0.2, 0.3]
        return DummyMatrix([[0.1, 0.2, 0.3] for _ in texts])

    def get_feature_names_out(self):
        # Feature names corresponding to the three terms
        return ["w1", "w2", "w3"]


@pytest.mark.asyncio
async def test_analyse_with_default_stop_words(monkeypatch):
    # Patch the vectorizer to our dummy version
    monkeypatch.setattr(tfidf_module, "TfidfVectorizer", DummyVectorizer)

    input_dtos = [
        TfidfInputDTO(file_name="file1.txt", text="dummy text1"),
        TfidfInputDTO(file_name="file2.txt", text="dummy text2"),
    ]
    results = await TextAnalysisTfidfService.analyse(input_dtos)

    # Check the result type and length
    assert isinstance(results, list)
    assert len(results) == len(input_dtos)

    # Expected DTOs based on our DummyVectorizer
    expected_words = [
        TfidfWordAnalysisDTO(word="w1", tf_score=0.1, idf_score=1.0, tf_idf_score=0.1),
        TfidfWordAnalysisDTO(word="w2", tf_score=0.2, idf_score=2.0, tf_idf_score=0.4),
        TfidfWordAnalysisDTO(word="w3", tf_score=0.3, idf_score=3.0, tf_idf_score=0.9),
    ]
    for result in results:
        assert isinstance(result, TfidfAnalysisResultDTO)
        # Compare each word DTO with approximate float comparison
        for actual, expected in zip(result.words, expected_words):
            assert actual.word == expected.word
            assert actual.tf_score == pytest.approx(expected.tf_score)
            assert actual.idf_score == pytest.approx(expected.idf_score)
            assert actual.tf_idf_score == pytest.approx(expected.tf_idf_score)


@pytest.mark.asyncio
async def test_analyse_with_custom_stop_words(monkeypatch):
    # Record what stop_words are passed to the vectorizer
    recorded = {}

    class RecordingDummyVectorizer(DummyVectorizer):
        def __init__(self, stop_words):
            super().__init__(stop_words)
            recorded["stop_words"] = stop_words

    monkeypatch.setattr(tfidf_module, "TfidfVectorizer", RecordingDummyVectorizer)

    custom_sw = {"foo", "bar"}
    input_dtos = [TfidfInputDTO(file_name="f.txt", text="text")]
    await TextAnalysisTfidfService.analyse(input_dtos, stop_words=custom_sw)

    assert recorded["stop_words"] == custom_sw


@pytest.mark.asyncio
async def test_empty_input_returns_empty_list():
    results = await TextAnalysisTfidfService.analyse([])
    assert isinstance(results, list)
    assert results == []


def test_tfidf_input_dto_validation():
    # Valid DTO should work
    dto = TfidfInputDTO(file_name="a.txt", text="hello")
    assert dto.file_name == "a.txt"
    assert dto.text == "hello"


def test_tfidf_input_dto_validation_errors():
    # Invalid types should raise ValidationError
    with pytest.raises(ValidationError):
        TfidfInputDTO(file_name=123, text='abc')
    with pytest.raises(ValidationError):
        TfidfInputDTO(file_name='abc', text=None)

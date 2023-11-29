import pytest
from src.whisperyt import DataProcessor

@pytest.fixture
def sample_dataframe():
    return DataProcessor.get_table("tests/test_output.json")

def test_get_table_columns(sample_dataframe):
    expected_columns = ['language', 'transcription', 'confidence', 'time_begin', 'time_end', 'speaker', 'channel']
    assert sample_dataframe.columns.to_list() == expected_columns

def test_get_table_not_none(sample_dataframe):
    assert sample_dataframe is not None

def test_get_table_not_empty(sample_dataframe):
    assert not sample_dataframe.empty


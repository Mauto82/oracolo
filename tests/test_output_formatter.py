import pytest
from presentation.output_formatter import OutputFormatter

@pytest.fixture
def formatter():
    return OutputFormatter()

def test_format_prediction(formatter):
    date = "01/01/2024"  # Usa il formato corretto DD/MM/YYYY
    wheel = "MI"
    numbers = [1, 2, 3, 4, 5]
    historical_data = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]

    result = formatter.format_prediction(date, wheel, numbers, historical_data)

    assert date in result
    assert wheel in result
    assert all(str(num).zfill(2) in result for num in numbers)

def test_format_prediction_no_history(formatter):
    date = "01/01/2024"
    wheel = "MI"
    numbers = [1, 2, 3, 4, 5]

    result = formatter.format_prediction(date, wheel, numbers, [])

    assert date in result
    assert wheel in result
    assert all(str(num).zfill(2) in result for num in numbers)
    assert "Statistiche Storiche" not in result

def test_format_error(formatter):
    error_msg = "Test error"
    result = formatter.format_error(error_msg)
    assert error_msg in result
    assert "Errore" in result
# tests/test_format_converter.py
import pytest
import pandas as pd
from io import StringIO
from services.format_converter import FormatConverter
from config import Config

@pytest.fixture
def sample_historical_data():
    """Fornisce dati di esempio nel formato storico"""
    return StringIO("""2024/01/01\tBA\t58\t22\t47\t49\t69
2024/01/01\tRM\t73\t24\t4\t39\t22
2024/01/01\tMI\t40\t38\t57\t67\t7""")

@pytest.fixture
def expected_converted_data():
    """Fornisce i dati attesi dopo la conversione"""
    return pd.DataFrame({
        'data': ['01/01/2024', '01/01/2024', '01/01/2024'],
        'ruota': ['BA', 'RO', 'MI'],
        'n1': [58, 73, 40],
        'n2': [22, 24, 38],
        'n3': [47, 4, 57],
        'n4': [49, 39, 67],
        'n5': [69, 22, 7]
    })

@pytest.fixture
def converter():
    """Fornisce un'istanza del convertitore"""
    return FormatConverter(Config())

def test_convert_format(converter, sample_historical_data, expected_converted_data, tmp_path):
    """Testa la conversione base del formato"""
    output_file = tmp_path / "test_output.csv"

    # Esegui la conversione
    converter.convert_lotto_format(sample_historical_data, output_file)

    # Leggi il file convertito
    result = pd.read_csv(
        output_file,
        delimiter=';',
        keep_default_na=False
    )

    # Verifica che i dati corrispondano
    pd.testing.assert_frame_equal(
        result,
        expected_converted_data,
        check_dtype=False  # Ignora le differenze di tipo (string vs object)
    )

def test_convert_invalid_input(converter, tmp_path):
    """Testa la gestione di input non validi"""
    output_file = tmp_path / "test_output.csv"
    invalid_input = StringIO("invalid,data,format")

    with pytest.raises(Exception):
        converter.convert_lotto_format(invalid_input, output_file)

def test_convert_empty_input(converter, tmp_path):
    """Testa la gestione di input vuoto"""
    output_file = tmp_path / "test_output.csv"
    empty_input = StringIO("")

    with pytest.raises(Exception):
        converter.convert_lotto_format(empty_input, output_file)

def test_convert_malformed_date(converter, tmp_path):
    """Testa la gestione di date malformate"""
    output_file = tmp_path / "test_output.csv"
    malformed_data = StringIO("invalid/date\tBA\t58\t22\t47\t49\t69")

    with pytest.raises(Exception):
        converter.convert_lotto_format(malformed_data, output_file)

def test_convert_invalid_wheel(converter, tmp_path):
    """Testa la gestione di ruote non valide"""
    output_file = tmp_path / "test_output.csv"
    invalid_wheel_data = StringIO("2024/01/01\tXX\t58\t22\t47\t49\t69")

    # Dovrebbe convertire comunque, la validazione delle ruote non è responsabilità del convertitore
    converter.convert_lotto_format(invalid_wheel_data, output_file)
    result = pd.read_csv(output_file, delimiter=';', keep_default_na=False)
    assert 'XX' in result['ruota'].values
# tests/test_format_converter.py
import pytest
import pandas as pd
from io import StringIO
from pathlib import Path
from services.format_converter import FormatConverter
from config import Config

@pytest.fixture
def sample_historical_data():
    """Fornisce dati di esempio nel formato storico"""
    return StringIO("""2024/01/01\tBA\t58\t22\t47\t49\t69
2024/01/01\tRM\t73\t24\t4\t39\t22
2024/01/01\tMI\t40\t38\t57\t67\t7
2024/01/02\tNA\t85\t44\t48\t88\t55
2024/01/02\tFI\t27\t57\t81\t43\t61""")

@pytest.fixture
def expected_converted_data():
    """Fornisce i dati attesi dopo la conversione"""
    return pd.DataFrame({
        'data': ['01/01/2024', '01/01/2024', '01/01/2024', '02/01/2024', '02/01/2024'],
        'ruota': ['BA', 'RO', 'MI', 'NA', 'FI'],
        'n1': [58, 73, 40, 85, 27],
        'n2': [22, 24, 38, 44, 57],
        'n3': [47, 4, 57, 48, 81],
        'n4': [49, 39, 67, 88, 43],
        'n5': [69, 22, 7, 55, 61]
    })

@pytest.fixture
def converter(tmp_path):
    """Fornisce un'istanza del convertitore con configurazione di test"""
    config = Config()
    config.HISTORICAL_SOURCE_FILE = str(tmp_path / "test_input.txt")
    config.HISTORICAL_OUTPUT_FILE = str(tmp_path / "test_output.csv")
    return FormatConverter(config)

def test_convert_format_basic(converter, sample_historical_data, expected_converted_data, tmp_path):
    """Testa la conversione base del formato"""
    output_file = tmp_path / "test_output.csv"
    converter.convert_lotto_format(sample_historical_data, output_file)

    result = pd.read_csv(output_file, delimiter=';', keep_default_na=False)
    pd.testing.assert_frame_equal(result, expected_converted_data, check_dtype=False)

def test_convert_rm_to_ro_mapping(converter, tmp_path):
    """Testa la corretta conversione da RM a RO"""
    input_data = StringIO("2024/01/01\tRM\t1\t2\t3\t4\t5")
    output_file = tmp_path / "test_output.csv"

    converter.convert_lotto_format(input_data, output_file)
    result = pd.read_csv(output_file, delimiter=';', keep_default_na=False)

    assert 'RO' in result['ruota'].values
    assert 'RM' not in result['ruota'].values

def test_convert_date_format(converter, tmp_path):
    """Testa la corretta conversione del formato data"""
    input_data = StringIO("2024/01/01\tMI\t1\t2\t3\t4\t5")
    output_file = tmp_path / "test_output.csv"

    converter.convert_lotto_format(input_data, output_file)
    result = pd.read_csv(output_file, delimiter=';', keep_default_na=False)

    assert result['data'].iloc[0] == '01/01/2024'

def test_convert_multiple_dates(converter, tmp_path):
    """Testa la conversione con multiple date"""
    input_data = StringIO("""2024/01/01\tMI\t1\t2\t3\t4\t5
2024/02/01\tBA\t6\t7\t8\t9\t10""")
    output_file = tmp_path / "test_output.csv"

    converter.convert_lotto_format(input_data, output_file)
    result = pd.read_csv(output_file, delimiter=';', keep_default_na=False)

    assert len(result) == 2
    assert set(result['data'].values) == {'01/01/2024', '01/02/2024'}

def test_convert_preserve_numbers(converter, tmp_path):
    """Testa che i numeri vengano preservati correttamente"""
    input_data = StringIO("2024/01/01\tMI\t1\t22\t33\t44\t90")
    output_file = tmp_path / "test_output.csv"

    converter.convert_lotto_format(input_data, output_file)
    result = pd.read_csv(output_file, delimiter=';', keep_default_na=False)

    expected_numbers = [1, 22, 33, 44, 90]
    actual_numbers = [result['n1'].iloc[0], result['n2'].iloc[0],
                     result['n3'].iloc[0], result['n4'].iloc[0],
                     result['n5'].iloc[0]]
    assert actual_numbers == expected_numbers

def test_convert_invalid_date_format(converter, tmp_path):
    """Testa la gestione di date in formato non valido"""
    input_data = StringIO("2024-01-01\tMI\t1\t2\t3\t4\t5")
    output_file = tmp_path / "test_output.csv"

    with pytest.raises(Exception) as exc_info:
        converter.convert_lotto_format(input_data, output_file)
    assert "parsing del file" in str(exc_info.value)

def test_convert_missing_fields(converter, tmp_path):
    """Testa la gestione di righe con campi mancanti"""
    input_data = StringIO("2024/01/01\tMI\t1\t2\t3")
    output_file = tmp_path / "test_output.csv"

    with pytest.raises(Exception) as exc_info:
        converter.convert_lotto_format(input_data, output_file)
    assert "parsing del file" in str(exc_info.value)

def test_convert_invalid_numbers(converter, tmp_path):
    """Testa la gestione di numeri non validi"""
    input_data = StringIO("2024/01/01\tMI\tabc\t2\t3\t4\t5")
    output_file = tmp_path / "test_output.csv"

    with pytest.raises(Exception) as exc_info:
        converter.convert_lotto_format(input_data, output_file)
    assert "parsing del file" in str(exc_info.value)

def test_convert_file_not_found(converter):
    """Testa la gestione di file non esistente"""
    with pytest.raises(Exception) as exc_info:
        converter.convert_lotto_format("file_non_esistente.txt", "output.csv")
    assert "file" in str(exc_info.value).lower()

def test_convert_invalid_output_path(converter, sample_historical_data):
    """Testa la gestione di percorso di output non valido"""
    with pytest.raises(Exception) as exc_info:
        converter.convert_lotto_format(sample_historical_data, "/invalid/path/output.csv")
    assert "file" in str(exc_info.value).lower()

def test_convert_permission_error(converter, sample_historical_data, tmp_path, monkeypatch):
    """Testa la gestione di errori di permesso"""
    output_file = tmp_path / "test_output.csv"

    def mock_to_csv(*args, **kwargs):
        raise PermissionError("Permission denied")

    # Patch il metodo to_csv di pandas DataFrame
    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    with pytest.raises(Exception) as exc_info:
        converter.convert_lotto_format(sample_historical_data, output_file)
    assert "permission" in str(exc_info.value).lower()
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

def test_convert_invalid_date_format(converter, tmp_path):
    """Testa la gestione di date in formato non valido"""
    input_data = StringIO("2024-01-01\tMI\t1\t2\t3\t4\t5")
    output_file = tmp_path / "test_output.csv"

    with pytest.raises(Exception) as exc_info:
        converter.convert_lotto_format(input_data, output_file)
    assert "time data" in str(exc_info.value)  # Verifica solo che sia un errore di parsing della data

def test_convert_missing_fields(converter, tmp_path):
    """Testa la gestione di righe con campi mancanti"""
    input_data = StringIO("2024/01/01\tMI\t1\t2\t3")
    output_file = tmp_path / "test_output.csv"

    # Non dovrebbe sollevare eccezioni - pandas gestisce i campi mancanti
    converter.convert_lotto_format(input_data, output_file)

    # Verifica che il file di output sia stato creato
    assert output_file.exists()

    # Leggi il file di output e verifica che i campi mancanti siano vuoti
    df = pd.read_csv(output_file, delimiter=';', keep_default_na=False)
    assert df['n4'].iloc[0] == ''  # Il quarto numero dovrebbe essere vuoto
    assert df['n5'].iloc[0] == ''  # Il quinto numero dovrebbe essere vuoto

def test_convert_invalid_numbers(converter, tmp_path):
    """Testa la gestione di numeri non validi"""
    input_data = StringIO("2024/01/01\tMI\tabc\t2\t3\t4\t5")
    output_file = tmp_path / "test_output.csv"

    # Non dovrebbe sollevare eccezioni - pandas gestisce i valori non numerici
    converter.convert_lotto_format(input_data, output_file)

    # Verifica che il file di output sia stato creato
    assert output_file.exists()

    # Leggi il file e verifica che il valore non numerico sia stato preservato
    df = pd.read_csv(output_file, delimiter=';', keep_default_na=False)
    assert df['n1'].iloc[0] == 'abc'  # Il valore non numerico dovrebbe essere preservato come stringa
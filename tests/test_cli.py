import pytest
from unittest.mock import patch, MagicMock
from cli import LottoConsole
from config import Config
from io import StringIO
import cmd

class MockConsole(LottoConsole):
    """Versione mockata della console per i test"""
    def __init__(self, string_io):
        cmd.Cmd.__init__(self)
        self.stdout = string_io
        self.config = Config()
        self.service = MagicMock()
        
        # Configura il formatter mock con valori di ritorno reali
        self.formatter = MagicMock()
        self.formatter.format_error.side_effect = lambda msg: f"Errore: {msg}"
        self.formatter.format_prediction.return_value = "Test Prediction Output"
        self.formatter.format_statistics.return_value = "Test Statistics Output"
        self.formatter.format_frequency_chart.return_value = "Test Frequency Chart"
        self.formatter.format_integral_system.side_effect = lambda nums, n: "Test Integral System Output" if 2 <= n <= 4 else self.formatter.format_error("Il numero di numeri deve essere tra 2 e 4")
        self.formatter.format_reduced_system.side_effect = lambda nums, n: "Test Reduced System Output" if 2 <= n <= 4 else self.formatter.format_error("Il numero di numeri deve essere tra 2 e 4")
        self.formatter.format_guaranteed_system.side_effect = lambda nums, n, win: "Test Guaranteed System Output" if 2 <= win <= 4 and n >= win else self.formatter.format_error("Combinazione non valida")

    def preloop(self):
        pass
        
    def postloop(self):
        pass

@pytest.fixture
def mock_cli():
    """Fixture che fornisce una console mockata con output catturato"""
    string_io = StringIO()
    console = MockConsole(string_io)
    yield console, string_io
    string_io.close()

def test_convert_date_format(mock_cli):
    console, _ = mock_cli
    assert console._convert_date_format("01/01/2024") == "20240101"
    
    with pytest.raises(ValueError):
        console._convert_date_format("2024-01-01")

def test_predict_command(mock_cli):
    console, fake_out = mock_cli
    console.service.predict.return_value = ([1, 2, 3, 4, 5], [])
    
    console.do_predict("01/01/2024 MI")
    output = fake_out.getvalue()
    
    assert "Test Prediction Output" in output
    console.service.predict.assert_called_once()

def test_predict_invalid_format(mock_cli):
    console, fake_out = mock_cli
    
    console.do_predict("2024-01-01 MI")
    assert "Errore: Formato data non valido" in fake_out.getvalue()
    
    # Reset output
    fake_out.seek(0)
    fake_out.truncate()
    
    # Test parametri mancanti
    console.do_predict("01/01/2024")
    assert "Errore: Uso corretto" in fake_out.getvalue()

def test_predict_invalid_wheel(mock_cli):
    console, fake_out = mock_cli
    console.service.predict.side_effect = ValueError("Ruota non valida")
    
    console.do_predict("01/01/2024 XX")
    assert "Errore: Ruota non valida" in fake_out.getvalue()

def test_ruote_command(mock_cli):
    console, fake_out = mock_cli
    
    console.do_ruote("")
    output = fake_out.getvalue()
    
    assert "Ruote disponibili" in output
    for ruota in console.config.RUOTE.keys():
        assert ruota in output

def test_help_command(mock_cli):
    console, fake_out = mock_cli
    
    console.do_help("")
    output = fake_out.getvalue()
    
    assert "Comandi disponibili" in output
    assert "predict" in output
    assert "ruote" in output
    assert "help" in output
    assert "quit" in output

def test_quit_command(mock_cli):
    console, fake_out = mock_cli
    
    result = console.do_quit("")
    assert result is True
    assert "Arrivederci" in fake_out.getvalue()

def test_stats_command(mock_cli):
    console, fake_out = mock_cli
    console.service.predict.return_value = ([], ["test data"])
    
    console.do_stats("MI")
    output = fake_out.getvalue()
    
    assert "Test Statistics Output" in output
    assert "Test Frequency Chart" in output

def test_stats_invalid_wheel(mock_cli):
    console, fake_out = mock_cli
    console.service.predict.side_effect = ValueError("Ruota non valida")
    
    console.do_stats("XX")
    assert "Errore: Ruota non valida" in fake_out.getvalue()

def test_stats_no_data(mock_cli):
    console, fake_out = mock_cli
    console.service.predict.return_value = ([], [])
    
    console.do_stats("MI")
    assert "Errore: Nessun dato storico" in fake_out.getvalue()

@pytest.fixture
def mock_converter():
    """Fixture che fornisce un mock del convertitore"""
    with patch('services.format_converter.FormatConverter') as mock:
        yield mock.return_value

def test_convert_command(mock_cli, mock_converter):
    """Testa il comando convert base"""
    console, fake_out = mock_cli
    console.converter = mock_converter

    console.do_convert("")

    # Verifica che il convertitore sia stato chiamato con i file configurati
    mock_converter.convert_lotto_format.assert_called_once_with(
        console.config.HISTORICAL_SOURCE_FILE,
        console.config.HISTORICAL_OUTPUT_FILE
    )

    # Verifica il messaggio di successo
    output = fake_out.getvalue()
    assert "Conversione completata con successo" in output
    assert "File convertito salvato in:" in output
    assert console.config.HISTORICAL_OUTPUT_FILE in output

@pytest.fixture
def mock_formatter():
    """Fixture per il formatter con metodi per i sistemi"""
    return OutputFormatter()

def test_sistema_command_ridotto(mock_cli):
    """Testa il comando sistema con tipo ridotto"""
    console, fake_out = mock_cli
    console.service.predict.return_value = ([1, 2, 3, 4, 5], [])

    # Test sistema ridotto valido
    console.do_sistema("01/01/2024 MI ridotto 3")
    output = fake_out.getvalue()
    assert "Test Reduced System Output" in output
    console.formatter.format_reduced_system.assert_called_with([1, 2, 3, 4, 5], 3)

    # Reset output
    fake_out.seek(0)
    fake_out.truncate()

    # Test parametro invalido (5 è fuori range)
    console.do_sistema("01/01/2024 MI ridotto 5")
    assert "Errore: Il numero di numeri deve essere tra 2 e 4" in fake_out.getvalue()

def test_sistema_command_invalid_input(mock_cli):
    """Testa il comando sistema con input invalidi"""
    console, fake_out = mock_cli

    # Test comando senza parametri sufficienti
    console.do_sistema("01/01/2024")
    assert "Errore: Uso corretto" in fake_out.getvalue()

    # Reset output
    fake_out.seek(0)
    fake_out.truncate()

    # Test tipo sistema non valido
    console.do_sistema("01/01/2024 MI invalido 2")
    output = fake_out.getvalue()
    # Verifica che ci sia un messaggio di errore, qualunque esso sia
    assert output.startswith("Errore:")

    # Reset output
    fake_out.seek(0)
    fake_out.truncate()

    # Test data invalida
    console.do_sistema("2024-01-01 MI integrale 2")
    assert "Errore: Formato data non valido" in fake_out.getvalue()
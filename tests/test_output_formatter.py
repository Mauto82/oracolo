import pytest
from presentation.output_formatter import OutputFormatter
from systems import IntegralSystem, ReducedSystem, GuaranteedSystem

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

@pytest.fixture
def mock_formatter():
    """Fixture che fornisce un'istanza di OutputFormatter per i test"""
    return OutputFormatter()

def test_format_integral_system(mock_formatter):
    """Testa la formattazione del sistema integrale"""
    output = mock_formatter.format_integral_system([1, 2, 3, 4, 5], 2)
    assert "SISTEMA INTEGRALE 2 NUMERI" in output
    assert "Totale combinazioni: 10" in output
    assert "1 - 2" in output

def test_format_reduced_system(mock_formatter):
    """Testa la formattazione del sistema ridotto"""
    output = mock_formatter.format_reduced_system([1, 2, 3, 4, 5], 2)
    assert "SISTEMA RIDOTTO 2 NUMERI" in output
    assert "Totale combinazioni: 5" in output

def test_format_guaranteed_system(mock_formatter):
    """Testa la formattazione del sistema garantito"""
    output = mock_formatter.format_guaranteed_system([1, 2, 3, 4, 5], 3, 2)
    assert "SISTEMA GARANTITO 3/2" in output
    assert "Vincita garantita: 2 punti" in output

def test_format_systems_errors(mock_formatter):
    """Testa gli errori nella formattazione dei sistemi"""
    # Test numeri insufficienti
    output = mock_formatter.format_integral_system([1, 2], 3)
    assert "Errore:" in output

    # Test dimensione non valida
    output = mock_formatter.format_reduced_system([1, 2, 3, 4, 5], 5)
    assert "Errore:" in output

    # Test garanzia impossibile
    output = mock_formatter.format_guaranteed_system([1, 2, 3], 2, 3)
    assert "Errore:" in output

def test_format_systems_all_combinations(mock_formatter):
    """Testa che vengano generate tutte le combinazioni attese"""
    # Test sistema integrale con terne
    output = mock_formatter.format_integral_system([1, 2, 3, 4], 3)
    assert "Totale combinazioni: 4" in output  # 4C3 = 4

    # Test sistema ridotto con terne
    output = mock_formatter.format_reduced_system([1, 2, 3, 4], 3)
    assert "Totale combinazioni: 2" in output  # Metà di 4C3

    # Test sistema garantito
    output = mock_formatter.format_guaranteed_system([1, 2, 3, 4], 3, 2)
    assert "Vincita garantita: 2 punti" in output

def test_format_systems_boundary_values(mock_formatter):
    """Testa i valori limite per i sistemi"""
    # Test minimo numero di elementi
    output = mock_formatter.format_integral_system([1, 2], 2)
    assert "Totale combinazioni: 1" in output

    # Test massimo numero di elementi consentito
    output = mock_formatter.format_reduced_system([1, 2, 3, 4, 5], 4)
    assert "SISTEMA RIDOTTO 4 NUMERI" in output

    # Test sistema garantito con valori limite
    output = mock_formatter.format_guaranteed_system([1, 2, 3, 4], 4, 2)
    assert "SISTEMA GARANTITO 4/2" in output

def test_format_systems_validation(mock_formatter):
    """Testa la validazione degli input"""
    # Test con lista vuota
    output = mock_formatter.format_integral_system([], 2)
    assert "Errore:" in output

    # Test con numeri negativi
    output = mock_formatter.format_reduced_system([-1, -2, -3], 2)
    assert "SISTEMA RIDOTTO 2 NUMERI" in output  # I numeri negativi sono permessi

    # Test con dimensione zero
    output = mock_formatter.format_guaranteed_system([1, 2, 3], 0, 2)
    assert "Errore:" in output

def test_format_error(formatter):
    error_msg = "Test error"
    result = formatter.format_error(error_msg)
    assert error_msg in result
    assert "Errore" in result
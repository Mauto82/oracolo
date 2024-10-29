import pytest
import pandas as pd
import numpy as np
from services.lotto_service import LottoService

def test_predict_invalid_wheel(trained_service):
    with pytest.raises(ValueError) as excinfo:
        trained_service.predict("20240101", "XX")
    assert "Ruota non valida" in str(excinfo.value)

def test_predict_valid_input(trained_service):
    prediction, historical_data = trained_service.predict("20240101", "MI")

    # Verifica la prediction
    assert len(prediction) == 5
    assert all(isinstance(x, (int, np.integer)) for x in prediction)
    assert all(0 <= x <= 90 for x in prediction)

def test_prepare_data(trained_service, sample_data):
    X, y = trained_service.prepare_data()

    assert list(X.columns) == ['data', 'ruota']
    assert list(y.columns) == ['n1', 'n2', 'n3', 'n4', 'n5']
    assert len(X) == len(sample_data)
import pytest
import pandas as pd
import numpy as np
from services.lotto_service import LottoService

def test_prepare_data(lotto_service, sample_data, monkeypatch):
    # Converti la data in datetime
    sample_data['data'] = pd.to_datetime(sample_data['data'], format='%d/%m/%Y')

    def mock_load_data():
        return sample_data

    monkeypatch.setattr(lotto_service.data_loader, 'load_data', mock_load_data)
    X, y = lotto_service.prepare_data()

    assert list(X.columns) == ['data', 'ruota']
    assert list(y.columns) == ['n1', 'n2', 'n3', 'n4', 'n5']

def test_predict_invalid_wheel(lotto_service):
    with pytest.raises(KeyError):
        lotto_service.predict("20240101", "XX")

def test_predict_valid_input(lotto_service):
    # Prima addestra il modello con dati di esempio
    sample_X = pd.DataFrame({
        'data': ['01012024', '02012024'],
        'ruota': [5, 6]
    })
    sample_y = pd.DataFrame({
        'n1': [1, 11],
        'n2': [2, 12],
        'n3': [3, 13],
        'n4': [4, 14],
        'n5': [5, 15]
    })
    lotto_service.predictor.train(sample_X, sample_y)

    prediction = lotto_service.predict("20240101", "MI")
    assert len(prediction) == 5
    assert all(isinstance(x, (int, np.integer)) for x in prediction)
    assert all(0 <= x <= 90 for x in prediction)
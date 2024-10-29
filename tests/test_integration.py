import pytest
import pandas as pd
import numpy as np
from config import Config
from services.lotto_service import LottoService

def test_full_prediction_flow(config, sample_data):
    """Test dell'intero flusso di predizione"""
    service = LottoService(config)
    service.initialize_predictor("decision_tree")

    # Prepara i dati di test
    sample_data['data'] = pd.to_datetime(sample_data['data'], format='%d/%m/%Y')
    def mock_load_data():
        return sample_data

    service.data_loader.load_data = mock_load_data
    service.train_model()

    # Scompatta il tuple restituito
    prediction, historical_data = service.predict("20240101", "MI")

    # Verifica la prediction
    assert len(prediction) == 5
    assert all(isinstance(x, (int, np.integer)) for x in prediction)
    assert all(0 <= x <= 90 for x in prediction)

    # Verifica i dati storici
    assert isinstance(historical_data, list)
    assert len(historical_data) > 0
    assert all(len(extract) == 5 for extract in historical_data)
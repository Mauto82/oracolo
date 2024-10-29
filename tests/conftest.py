import pytest
import pandas as pd
import numpy as np
from config import Config
from services.lotto_service import LottoService
from data.data_loader import DataLoader

@pytest.fixture
def sample_data():
    """Fornisce dati di esempio nel formato originale (stringhe per le ruote)"""
    return pd.DataFrame({
        'data': ['01/01/2024', '02/01/2024'],
        'ruota': ['MI', 'NA'],  # Ruote come stringhe
        'n1': [1, 11],
        'n2': [2, 12],
        'n3': [3, 13],
        'n4': [4, 14],
        'n5': [5, 15]
    })

@pytest.fixture
def processed_sample_data(config, sample_data):
    """Fornisce dati di esempio già processati correttamente"""
    df = sample_data.copy()
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['ruota'] = df['ruota'].map(config.RUOTE)  # Usa il mapping corretto dal config
    return df

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def trained_service(config, sample_data):  # Usa sample_data invece di processed_sample_data
    """Fornisce un servizio già inizializzato e addestrato"""
    service = LottoService(config)
    service.initialize_predictor("decision_tree")

    def mock_load_data():
        return sample_data  # Usa i dati non processati

    service.data_loader.load_data = mock_load_data
    service.train_model()
    return service
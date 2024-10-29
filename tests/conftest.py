import pytest
import pandas as pd
from datetime import datetime
from config import Config
from data.data_loader import DataLoader
from services.lotto_service import LottoService
from predictors.predictor_factory import PredictorFactory

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'data': ['01/01/2024', '02/01/2024'],
        'ruota': ['MI', 'NA'],
        'n1': [1, 11],
        'n2': [2, 12],
        'n3': [3, 13],
        'n4': [4, 14],
        'n5': [5, 15]
    })

@pytest.fixture
def data_loader(config):
    return DataLoader(config)

@pytest.fixture
def lotto_service(config):
    service = LottoService(config)
    service.initialize_predictor("decision_tree")
    return service
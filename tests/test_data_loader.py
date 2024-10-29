import pytest
import pandas as pd
import numpy as np
from data.data_loader import DataLoader
from datetime import datetime

def test_format_dates(data_loader, sample_data):
    # Converti prima in datetime
    sample_data['data'] = pd.to_datetime(sample_data['data'], format='%d/%m/%Y')
    processed_df = data_loader._format_dates(sample_data)
    assert processed_df['data'].tolist() == ['01012024', '02012024']

def test_preprocess_data(data_loader, sample_data):
    # Converti prima in datetime
    sample_data['data'] = pd.to_datetime(sample_data['data'], format='%d/%m/%Y')
    processed_df = data_loader.preprocess_data(sample_data.copy())
    assert processed_df.ruota.tolist() == [5, 6]  # MI = 5, NA = 6
    assert isinstance(processed_df['data'].iloc[0], str)
    assert processed_df['data'].iloc[0] == '01012024'
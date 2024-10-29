# app/data/data_loader.py
from typing import List
import pandas as pd
from datetime import datetime
from models.extraction import Extraction
from config import Config

class DataLoader:
    def __init__(self, config: Config):
        self.config = config

    def load_data(self) -> pd.DataFrame:
        """Factory method per caricare i dati"""
        # Leggiamo prima il CSV con la colonna data come oggetto
        df = pd.read_csv(
            self.config.CSV_FILE,
            delimiter=self.config.CSV_DELIMITER,
            keep_default_na=False
        )

        # Convertiamo la colonna data usando to_datetime
        df['data'] = pd.to_datetime(
            df['data'],
            format=self.config.DATE_FORMAT
        )

        return df

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Template method per il preprocessing dei dati"""
        df = self._convert_wheel_to_numeric(df)
        df = self._format_dates(df)
        return df

    def _convert_wheel_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        df.ruota = [self.config.RUOTE[item] for item in df.ruota]
        return df

    def _format_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        df['data'] = df['data'].dt.strftime('%d%m%Y')
        return df
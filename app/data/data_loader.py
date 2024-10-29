from typing import List
import pandas as pd
from datetime import datetime
from models.extraction import Extraction
from config import Config

class DataLoader:
    def __init__(self, config: Config):
        self.config = config

    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(
            self.config.CSV_FILE,
            delimiter=self.config.CSV_DELIMITER,
            keep_default_na=False
        )

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()  # Crea una copia per evitare warning
        df = self._convert_wheel_to_numeric(df)
        df['data'] = pd.to_datetime(df['data'], format=self.config.DATE_FORMAT)
        df['data'] = df['data'].dt.strftime('%Y%m%d')
        return df

    def _convert_wheel_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """Converte i codici delle ruote in valori numerici"""
        # Se la ruota è già numerica, non fare nulla
        if pd.api.types.is_numeric_dtype(df['ruota']):
            return df

        # Altrimenti converti da stringa a numero
        df['ruota'] = df['ruota'].apply(lambda x: self.config.RUOTE.get(x, 0))
        return df
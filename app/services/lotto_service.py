from typing import List, Tuple, Dict
import pandas as pd
from config import Config
from data.data_loader import DataLoader
from predictors.predictor_interface import PredictorInterface
from predictors.predictor_factory import PredictorFactory

class LottoService:
    def __init__(self, config: Config):
        self.config = config
        self.data_loader = DataLoader(config)
        self.predictor: PredictorInterface = None
        self.historical_data: Dict = {}

    def initialize_predictor(self, predictor_type: str) -> None:
        self.predictor = PredictorFactory.create_predictor(predictor_type)

    def prepare_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df = self.data_loader.load_data()
        df = self.data_loader.preprocess_data(df)

        # Salva i dati storici per ruota
        self._prepare_historical_data(df)

        X = df.drop(columns=['n1','n2','n3','n4','n5'])
        y = df.drop(columns=['data', 'ruota'])

        return X, y

    def _prepare_historical_data(self, df: pd.DataFrame) -> None:
        """Prepara i dati storici organizzati per ruota"""
        for wheel_name, ruota_code in self.config.RUOTE.items():
            ruota_data = df[df['ruota'] == ruota_code]
            self.historical_data[wheel_name] = [
                [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
                for _, row in ruota_data.iterrows()
            ]

    def train_model(self) -> None:
        if not self.predictor:
            raise ValueError("Predictor not initialized")

        X, y = self.prepare_data()
        self.predictor.train(X, y)

    def predict(self, date: str, wheel: str) -> Tuple[List[int], Dict]:
        """
        Effettua una predizione per una data e ruota specifiche

        Args:
            date: Data in formato YYYYMMDD
            wheel: Codice della ruota (es. 'MI', 'RO', etc.)

        Returns:
            Tuple[List[int], Dict]: Lista dei numeri predetti e dati storici della ruota
        """
        if not self.predictor:
            raise ValueError("Predictor not initialized")

        wheel_upper = wheel.upper().replace('RM', 'RO')
        if wheel_upper not in self.config.RUOTE:
            raise ValueError(f"Ruota non valida: {wheel}. Ruote valide: {', '.join(self.config.RUOTE.keys())}")

        wheel_code = self.config.RUOTE[wheel_upper]
        prediction = self.predictor.predict([date, wheel_code])

        return prediction, self.historical_data.get(wheel_upper, [])
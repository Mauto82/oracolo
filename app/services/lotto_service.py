from typing import List, Tuple
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

    def initialize_predictor(self, predictor_type: str) -> None:
        self.predictor = PredictorFactory.create_predictor(predictor_type)

    def prepare_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df = self.data_loader.load_data()
        df = self.data_loader.preprocess_data(df)

        X = df.drop(columns=['n1','n2','n3','n4','n5'])
        y = df.drop(columns=['data', 'ruota'])

        return X, y

    def train_model(self) -> None:
        if not self.predictor:
            raise ValueError("Predictor not initialized")

        X, y = self.prepare_data()
        self.predictor.train(X, y)

    def predict(self, date: str, wheel: str) -> List[int]:
        if not self.predictor:
            raise ValueError("Predictor not initialized")

        wheel_code = self.config.RUOTE[wheel.upper().replace('RM', 'RO')]
        return self.predictor.predict([date, wheel_code])
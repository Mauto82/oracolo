from abc import ABC, abstractmethod
import pandas as pd
from typing import List

class PredictorInterface(ABC):
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def predict(self, features: List) -> List[int]:
        pass
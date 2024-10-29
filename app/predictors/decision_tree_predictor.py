from sklearn.tree import DecisionTreeClassifier
from predictors.predictor_interface import PredictorInterface
import pandas as pd
from typing import List

class DecisionTreePredictor(PredictorInterface):
    def __init__(self):
        self.model = DecisionTreeClassifier()

    def train(self, X: pd.DataFrame, y: pd.DataFrame) -> None:
        self.model.fit(X.values, y.values)

    def predict(self, features: List) -> List[int]:
        return self.model.predict([features])[0]
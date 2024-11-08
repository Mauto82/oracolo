from sklearn.tree import DecisionTreeClassifier
from predictors.predictor_interface import PredictorInterface
import pandas as pd
from typing import List

class DecisionTreePredictor(PredictorInterface):
    def __init__(self):
        """Inizializza il modello"""
        self.model = DecisionTreeClassifier()
        self.is_trained = False

    def train(self, X: pd.DataFrame, y: pd.DataFrame) -> None:
        """
        Addestra il modello sui dati forniti.

        Args:
            X: DataFrame con le feature (data, ruota)
            y: DataFrame con i target (n1, n2, n3, n4, n5)
        """
        try:
            self.model.fit(X.values, y.values)
            self.is_trained = True
        except Exception as e:
            raise ValueError(f"Errore durante il training: {str(e)}")

    def predict(self, features: List) -> List[int]:
        """
        Predice i numeri per le feature fornite.

        Args:
            features: Lista contenente [data, codice_ruota]

        Returns:
            List[int]: Lista dei 5 numeri predetti
        """
        if not self.is_trained:
            raise ValueError("Il modello non è stato ancora addestrato")

        try:
            prediction = self.model.predict([features])[0]
            return [int(num) for num in prediction]  # Converte in lista di interi
        except Exception as e:
            raise ValueError(f"Errore durante la predizione: {str(e)}")
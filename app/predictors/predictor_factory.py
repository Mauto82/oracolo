from predictors.predictor_interface import PredictorInterface
from predictors.decision_tree_predictor import DecisionTreePredictor

class PredictorFactory:
    @staticmethod
    def create_predictor(predictor_type: str) -> PredictorInterface:
        if predictor_type.lower() == "decision_tree":
            return DecisionTreePredictor()
        # Qui potremmo aggiungere altri tipi di predittori
        raise ValueError(f"Predictor type {predictor_type} not supported")
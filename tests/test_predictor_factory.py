import pytest
from predictors.predictor_factory import PredictorFactory
from predictors.predictor_interface import PredictorInterface

def test_create_decision_tree_predictor():
    predictor = PredictorFactory.create_predictor("decision_tree")
    assert isinstance(predictor, PredictorInterface)
    assert hasattr(predictor, 'train')
    assert hasattr(predictor, 'predict')

def test_invalid_predictor_type():
    with pytest.raises(ValueError):
        PredictorFactory.create_predictor("invalid_type")
import pytest
import numpy as np
import pandas as pd
from predictors.decision_tree_predictor import DecisionTreePredictor

def test_decision_tree_predictor_training():
    predictor = DecisionTreePredictor()
    X = pd.DataFrame({
        'data': ['01012024', '02012024'],
        'ruota': [1, 2]
    })
    y = pd.DataFrame({
        'n1': [1, 6],
        'n2': [2, 7],
        'n3': [3, 8],
        'n4': [4, 9],
        'n5': [5, 10]
    })
    predictor.train(X, y)

    prediction = predictor.predict(['01012024', 1])
    assert len(prediction) == 5
    assert all(isinstance(x, (int, np.integer)) for x in prediction)
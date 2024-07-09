import pytest
import numpy as np
from myinternshipcalculator2024.calculator import train_linear_regression

def test_train_linear_regression():
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([2, 3, 4, 5, 6])
    model = train_linear_regression(X, y)
    assert model is not None
    assert hasattr(model, 'predict')
    predictions = model.predict(X)
    assert len(predictions) == len(y)


# --- FILE: tests/test_train_model.py ---
import os
from model.train_model import grid_search, X, y

def test_grid_search_trained():
    assert hasattr(grid_search, "best_estimator_")
    assert grid_search.best_estimator_ is not None

def test_model_predict():
    model = grid_search.best_estimator_
    prediction = model.predict([X.iloc[0]])
    assert prediction.shape == (1,)

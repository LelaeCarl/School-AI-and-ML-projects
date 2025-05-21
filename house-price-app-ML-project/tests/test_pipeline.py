
# --- FILE: tests/test_pipeline.py ---
import pandas as pd
from model.pipeline import get_preprocessing_pipeline, NUM_FEATURES, CAT_FEATURES

def test_pipeline_transform():
    pipeline = get_preprocessing_pipeline()
    sample = pd.DataFrame([{
        "GrLivArea": 1500,
        "TotalBsmtSF": 1000,
        "YearBuilt": 2005,
        "FullBath": 2,
        "GarageCars": 2,
        "OverallQual": 7
    }])
    result = pipeline.fit_transform(sample)
    assert result.shape[0] == 1

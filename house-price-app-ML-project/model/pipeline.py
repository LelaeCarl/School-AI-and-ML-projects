
# --- FILE: model/pipeline.py ---
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Define numerical and categorical features
NUM_FEATURES = ['GrLivArea', 'TotalBsmtSF', 'YearBuilt', 'FullBath', 'GarageCars']
CAT_FEATURES = ['OverallQual']

def get_preprocessing_pipeline():
    numeric_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([
        ('num', numeric_pipeline, NUM_FEATURES),
        ('cat', categorical_pipeline, CAT_FEATURES)
    ])

    return preprocessor

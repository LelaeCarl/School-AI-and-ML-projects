
# --- FILE: model/train_model.py ---
import pandas as pd
import joblib
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from math import sqrt

from pipeline import get_preprocessing_pipeline, NUM_FEATURES, CAT_FEATURES
from config import Config
import os

# Set up logging
logging.basicConfig(filename=os.path.join(Config.LOG_DIR, 'train.log'), level=logging.INFO)

# Load dataset
data = pd.read_csv(r'C:\Users\Sage\Desktop\school-ai-and-ml-projects\house-price-app-ML-project\data\train.csv')
X = data[NUM_FEATURES + CAT_FEATURES]
y = data['SalePrice']

# Create pipeline
preprocessor = get_preprocessing_pipeline()
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# Hyperparameter tuning
params = {
    'regressor__n_estimators': [100, 200],
    'regressor__max_depth': [None, 10, 20]
}

grid_search = GridSearchCV(model, params, cv=5, scoring='neg_root_mean_squared_error', verbose=1)
grid_search.fit(X, y)

# Save best model
joblib.dump(grid_search.best_estimator_, Config.MODEL_PATH)

# Logging
best_rmse = -grid_search.best_score_
logging.info(f"Best RMSE: {best_rmse:.2f}")
logging.info(f"Best Parameters: {grid_search.best_params_}")

# Performance on test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
best_model = grid_search.best_estimator_
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)
rmse = sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
logging.info(f"Test RMSE: {rmse:.2f}, R²: {r2:.2f}")

print(f"Model saved to: {Config.MODEL_PATH}")
print(f"File exists: {os.path.exists(Config.MODEL_PATH)}, Size: {os.path.getsize(Config.MODEL_PATH)} bytes")

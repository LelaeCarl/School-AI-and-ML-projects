# --- FILE: model/generate_eda_assets.py ---
import matplotlib
matplotlib.use('Agg')  # Ensures plots can be saved without GUI

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import os

# === ABSOLUTE PATHS BASED ON PROJECT STRUCTURE ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

IMG_DIR = os.path.join(BASE_DIR, 'static', 'img')
JSON_DIR = os.path.join(BASE_DIR, 'static', 'data')

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# === Load Data ===
data = pd.read_csv(r'C:\Users\Sage\Desktop\school-ai-and-ml-projects\house-price-app-ML-project\data\train.csv')

# === Correlation Heatmap ===
plt.figure(figsize=(12, 10))
corr = data.corr(numeric_only=True)
sns.heatmap(corr, cmap='coolwarm', annot=False)
plt.title("Correlation Heatmap")
plt.tight_layout()
heatmap_path = os.path.join(IMG_DIR, "corr_heatmap.png")
plt.savefig(heatmap_path)
plt.close()
assert os.path.exists(heatmap_path), f"❌ Missing: {heatmap_path}"

# === Sale Price Distribution ===
plt.figure(figsize=(10, 6))
sns.histplot(data['SalePrice'], kde=True)
plt.title("Sale Price Distribution")
plt.xlabel("SalePrice")
dist_path = os.path.join(IMG_DIR, "price_distribution.png")
plt.savefig(dist_path)
plt.close()
assert os.path.exists(dist_path), f"❌ Missing: {dist_path}"

# === Mock Feature Importance Chart ===
features = ['GrLivArea', 'OverallQual', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt']
importances = [0.32, 0.24, 0.15, 0.12, 0.1, 0.07]
fi_fig = px.bar(x=features, y=importances, labels={'x': 'Feature', 'y': 'Importance'}, title='Mock Feature Importances')
feature_path = os.path.join(JSON_DIR, "feature_importance.json")
pio.write_json(fi_fig, feature_path)
assert os.path.exists(feature_path), f"❌ Missing: {feature_path}"

# === Sale Price Trend Over Time ===
price_trend = data.groupby("YearBuilt")["SalePrice"].mean().reset_index()
trend_fig = px.line(price_trend, x="YearBuilt", y="SalePrice", title="Average SalePrice Over Years")
trend_path = os.path.join(JSON_DIR, "price_trend.json")
pio.write_json(trend_fig, trend_path)
assert os.path.exists(trend_path), f"❌ Missing: {trend_path}"

# === Final Output ===
print("✅ EDA assets successfully generated:")
print(f"✔ {heatmap_path}")
print(f"✔ {dist_path}")
print(f"✔ {feature_path}")
print(f"✔ {trend_path}")

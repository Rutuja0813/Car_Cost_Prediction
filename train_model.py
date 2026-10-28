
import pickle
from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# =================================================
# 1. PROJECT PATHS
# =================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "car_data_expanded.csv"
MODEL_FILE = BASE_DIR / "car_price_model.pkl"


# =================================================
# 2. LOAD DATASET
# =================================================

print("=" * 50)
print("SMARTCAR - CAR PRICE PREDICTION")
print("=" * 50)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}\n"
        "Place car_data_expanded.csv in the "
        "same folder as train_model.py."
    )

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully!")
print("Original rows:", len(df))


# =================================================
# 3. CLEAN COLUMN NAMES
# =================================================

df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
)

required_columns = [
    "brand",
    "model",
    "year",
    "fuel",
    "transmission",
    "km_driven",
    "engine",
    "owners",
    "mileage",
    "price",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in dataset: {missing_columns}"
    )

df = df[required_columns].copy()


# =================================================
# 4. CLEAN DATA
# =================================================

categorical_columns = [
    "brand",
    "model",
    "fuel",
    "transmission",
]

numeric_columns = [
    "year",
    "km_driven",
    "engine",
    "owners",
    "mileage",
    "price",
]

# Clean text columns
for column in categorical_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df[column] = df[column].replace("", pd.NA)

# Convert numeric columns safely
for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )

# Remove rows with missing or invalid values
df = df.dropna(subset=required_columns)

# Keep only sensible positive prices and valid feature values
df = df[
    (df["price"] > 0)
    & (df["year"] >= 1900)
    & (df["km_driven"] >= 0)
    & (df["engine"] > 0)
    & (df["owners"] >= 0)
    & (df["mileage"] > 0)
]

# Remove duplicate records
df = df.drop_duplicates().reset_index(drop=True)

if len(df) < 10:
    raise ValueError(
        "Not enough valid records to train the model. "
        "Please check your CSV dataset."
    )

print("Rows after cleaning:", len(df))
print("Brands available:", df["brand"].nunique())
print("Car models available:", df["model"].nunique())


# =================================================
# 5. FEATURES AND TARGET
# =================================================

feature_columns = [
    "brand",
    "model",
    "year",
    "fuel",
    "transmission",
    "km_driven",
    "engine",
    "owners",
    "mileage",
]

X = df[feature_columns]
y = df["price"]


# =================================================
# 6. TRAIN / TEST SPLIT
# =================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# =================================================
# 7. PREPROCESSING
# =================================================

categorical_features = [
    "brand",
    "model",
    "fuel",
    "transmission",
]

numeric_features = [
    "year",
    "km_driven",
    "engine",
    "owners",
    "mileage",
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
        ),
        (
            "numeric",
            "passthrough",
            numeric_features,
        ),
    ]
)


# =================================================
# 8. RANDOM FOREST MODEL
# =================================================

random_forest = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    min_samples_leaf=2,
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", random_forest),
    ]
)


# =================================================
# 9. TRAIN MODEL
# =================================================

print("\nTraining Random Forest model...")

pipeline.fit(X_train, y_train)

print("Training completed successfully!")


# =================================================
# 10. EVALUATE MODEL
# =================================================

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n" + "=" * 40)
print("MODEL EVALUATION RESULTS")
print("=" * 40)

print(f"Mean Absolute Error (MAE): Rs. {mae:,.2f}")
print(f"R2 Score: {r2:.4f}")

print(
    "\nMAE is the average absolute difference "
    "between actual and predicted prices."
)

print(
    "R2 measures how well the model explains "
    "price variation on the test dataset."
)

print(
    "\nNote: Evaluation results depend on the quality "
    "and reliability of the dataset."
)


# =================================================
# 11. SAVE TRAINED MODEL
# =================================================

with open(MODEL_FILE, "wb") as file:
    pickle.dump(pipeline, file)

print("\n" + "=" * 50)
print("MODEL SAVED SUCCESSFULLY!")
print(f"Saved location: {MODEL_FILE}")
print("=" * 50)
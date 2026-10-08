# train.py
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset from a working source (Kaggle/hosted)
url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"
df = pd.read_csv(url)

print("✅ Columns:", df.columns.tolist())  # Debug print

# Prepare data
X = df[["Pregnancies", "Glucose", "BloodPressure", "BMI", "Age"]]
y = df["Outcome"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save
model_dir = Path(__file__).resolve().parent.parent / "model"
model_dir.mkdir(parents=True, exist_ok=True)
model_path = model_dir / "diabetes_model.pkl"
joblib.dump(model, model_path)
print(f"✅ Model saved to {model_path}")

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("datasets/disease_dataset.csv")

# Split features and target
X = df.drop("disease", axis=1)
y = df["disease"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "backend/disease_model.pkl")

print("Model trained and saved successfully!")
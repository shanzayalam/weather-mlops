import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import mlflow
import mlflow.sklearn

# Start MLFlow experiment
mlflow.set_experiment("Weather Prediction Pipeline")

# Load processed data
df = pd.read_csv("processed_data.csv")

# Feature and target split
X = df[["Humidity", "Wind Speed"]]
y = df["Temperature"]

# Train the model
model = LinearRegression()

with mlflow.start_run() as run:
    # Log parameters
    mlflow.log_param("features", ["Humidity", "Wind Speed"])
    mlflow.log_param("model_type", "LinearRegression")
    
    # Train and fit
    model.fit(X, y)
    
    # Log metrics
    r2_score = model.score(X, y)
    mlflow.log_metric("r2_score", r2_score)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Save model locally
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

print("Model trained, logged to MLFlow, and saved to model.pkl")

import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load processed data
df = pd.read_csv("processed_data.csv")

# Feature and target split
X = df[["Humidity", "Wind Speed"]]
y = df["Temperature"]

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved to model.pkl")

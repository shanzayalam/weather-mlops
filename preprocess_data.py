import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load raw data
df = pd.read_csv("raw_data.csv")

# Handle missing values
df.fillna(method="ffill", inplace=True)

# Normalize numerical fields
scaler = MinMaxScaler()
df[["Temperature", "Wind Speed"]] = scaler.fit_transform(df[["Temperature", "Wind Speed"]])

# Save processed data
df.to_csv("processed_data.csv", index=False)
print("Data preprocessing complete and saved to processed_data.csv")

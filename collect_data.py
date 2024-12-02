import requests
import pandas as pd
from datetime import datetime

API_KEY = "8b4bc5079f4044efcc9e87c75e1dfa5b"
CITY = "Islamabad"
URL = f"https://api.openweathermap.org/data/2.5/forecast?q=Islamabad&APPID=8b4bc5079f4044efcc9e87c75e1dfa5b"

response = requests.get(URL)
response = requests.get(URL)

if response.status_code == 200:
    print("API Key works!")
    print(response.json())
else:
    print(f"Error: {response.json()}")
data = response.json()

weather_data = []
for entry in data["list"]:
    weather_data.append({
        "Date": entry["dt_txt"],
        "Temperature": entry["main"]["temp"],
        "Humidity": entry["main"]["humidity"],
        "Wind Speed": entry["wind"]["speed"],
        "Weather Condition": entry["weather"][0]["description"]
    })

df = pd.DataFrame(weather_data)
df.to_csv("raw_data.csv", index=False)
print("Weather data collected and saved to raw_data.csv")

import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("OPENWEATHER_CITY", "Islamabad")  # Default to Islamabad if not set
URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&APPID={API_KEY}"

if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in environment variables. Please set it in .env file.")

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

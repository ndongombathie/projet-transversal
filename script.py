import requests
import pandas as pd
import time
import os

# API AirGradient
sensor_url = "https://api.airgradient.com/public/api/v1/locations/measures/current?token=66e22601-c57f-430b-8858-420dc7016083"

# API Key OpenWeather
API_KEY = os.getenv("OPENWEATHER_API_KEY")

stations = requests.get(sensor_url).json()

rows = []

for station in stations:

    lat = station.get("latitude")
    lon = station.get("longitude")
    
    # Filtre sur Thiès
    location_name = station.get("locationName")
    if "Thiès" not in location_name:
        continue

    # Ignorer les stations sans coordonnées
    if lat is None or lon is None:
        continue

    try:

        air_url = (
            f"https://api.openweathermap.org/data/2.5/air_pollution"
            f"?lat={lat}&lon={lon}"
            f"&appid={API_KEY}"
        )

        air_data = requests.get(air_url).json()

        pollutants = air_data["list"][0]["components"]

        merged = {
            "locationId": station.get("locationId"),
            "locationName": station.get("locationName"),
            "latitude": lat,
            "longitude": lon,
            "timestamp": station.get("timestamp"),

            "pm25": station.get("pm02_corrected"),
            "pm10": station.get("pm10_corrected"),
            "temperature": station.get("atmp_corrected"),
            "humidity": station.get("rhum_corrected"),
            "co2": station.get("rco2_corrected"),
            "tvoc": station.get("tvoc"),

            "co": pollutants.get("co"),
            "no": pollutants.get("no"),
            "no2": pollutants.get("no2"),
            "o3": pollutants.get("o3"),
            "so2": pollutants.get("so2"),
            "nh3": pollutants.get("nh3")
        }

        rows.append(merged)

        print(f"OK : {station.get('locationName')}")

        # éviter de dépasser le quota
        time.sleep(1)

    except Exception as e:
        print(
            f"Erreur {station.get('locationName')} : {e}"
        )

df = pd.DataFrame(rows)

print(df.head())

df.to_csv(
    "air_quality_dataset.csv",
    index=False
)
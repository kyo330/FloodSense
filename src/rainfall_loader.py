from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
import pandas as pd
import numpy as np

def fetch_current_rainfall_college_station():
    """
    Fetches the current rainfall for College Station, TX, for the past 7 days.
    """
    end_date = datetime.now().date()  # Current date
    start_date = end_date - timedelta(days=7)  # 7 days ago

    # Fetch historical precipitation data for College Station, TX
    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude=30.62798&longitude=-96.33441"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=precipitation"
        f"&timezone=America%2FChicago"  # Ensure time zone is set to America/Chicago
    )
    response = requests.get(url)
    data = response.json()

    # Ensure proper conversion of time to America/Chicago timezone
    times = [
        datetime.fromisoformat(t).replace(tzinfo=ZoneInfo("America/Chicago")) for t in data["hourly"]["time"]
    ]
    precipitation = data["hourly"]["precipitation"]

    # Create a DataFrame with the correct time and precipitation data
    df = pd.DataFrame({
        "datetime": times,
        "precipitation_mm": precipitation
    })

    return df


def simulate_rainfall_data(days=7, min_mm=10, max_mm=60):
    """
    Simulates rainfall over a given number of days using uniform distribution.
    """
    dates = [datetime.now().date() - timedelta(days=i) for i in range(days)]
    rainfall = np.random.uniform(low=min_mm, high=max_mm, size=days)
    df = pd.DataFrame({"date": dates, "rainfall_mm": rainfall})
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

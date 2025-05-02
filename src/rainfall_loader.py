import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def fetch_current_rainfall_college_station():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=30.62798&longitude=-96.33441"
        "&hourly=precipitation"
        "&timezone=America%2FChicago"
    )
    response = requests.get(url)
    data = response.json()

    latest_time = data["hourly"]["time"][-1]
    latest_rainfall = data["hourly"]["precipitation"][-1]
    return latest_time, latest_rainfall


def simulate_rainfall_data(days=7, min_mm=10, max_mm=60):
    """
    Simulates rainfall over a given number of days using uniform distribution.

    Args:
        days (int): Number of past days to simulate.
        min_mm (float): Minimum rainfall in mm.
        max_mm (float): Maximum rainfall in mm.

    Returns:
        pd.DataFrame: DataFrame with columns ['date', 'rainfall_mm']
    """
    dates = [datetime.now().date() - timedelta(days=i) for i in range(days)]
    rainfall = np.random.uniform(low=min_mm, high=max_mm, size=days)
    df = pd.DataFrame({"date": dates, "rainfall_mm": rainfall})
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

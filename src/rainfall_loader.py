from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
import pandas as pd
import numpy as np

def fetch_current_rainfall_college_station():
    """
    Fetches hourly precipitation data for College Station, TX for the past 7 days,
    with timestamps localized to America/Chicago timezone.
    """
    end_date = datetime.now(ZoneInfo("UTC")).date()
    start_date = end_date - timedelta(days=7)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude=30.62798&longitude=-96.33441"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=precipitation"
        f"&timezone=UTC"
    )

    response = requests.get(url)
    data = response.json()

    # Convert UTC to America/Chicago
    times_utc = [datetime.fromisoformat(t).replace(tzinfo=ZoneInfo("UTC")) for t in data["hourly"]["time"]]
    times_local = [dt.astimezone(ZoneInfo("America/Chicago")) for dt in times_utc]
    
    precipitation = data["hourly"]["precipitation"]

    df = pd.DataFrame({
        "datetime": times_local,
        "precipitation_mm": precipitation
    })

    return df

def simulate_rainfall_data(days=7, min_mm=10, max_mm=60):
    """
    Simulates rainfall data over a specified number of past days using a uniform distribution.
    """
    today = datetime.now(ZoneInfo("America/Chicago")).date()
    dates = [today - timedelta(days=i) for i in range(days)]
    rainfall = np.random.uniform(low=min_mm, high=max_mm, size=days)
    
    df = pd.DataFrame({"date": pd.to_datetime(dates), "rainfall_mm": rainfall})
    df = df.sort_values("date")
    return df

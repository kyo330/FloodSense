from datetime import datetime, timedelta
import pytz
import requests
import pandas as pd
import numpy as np

def fetch_current_rainfall_college_station():
    """
    Fetches hourly precipitation data for College Station, TX for the past 7 days,
    with timestamps localized to America/Chicago timezone.
    """
    utc = pytz.utc
    central = pytz.timezone('America/Chicago')

    end_date = datetime.utcnow().date()
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

    
    times_utc = [utc.localize(datetime.fromisoformat(t)) for t in data["hourly"]["time"]]
    times_local = [dt.astimezone(central) for dt in times_utc]

    df = pd.DataFrame({
        "datetime": times_local,
        "precipitation_mm": data["hourly"]["precipitation"]
    })

    return df

def simulate_rainfall_data(days=7, min_mm=10, max_mm=60):
    """
    Simulates rainfall data over a specified number of past days using a uniform distribution.
    """
    central = pytz.timezone('America/Chicago')
    today = datetime.now(central).date()

    dates = [today - timedelta(days=i) for i in range(days)]
    rainfall = np.random.uniform(low=min_mm, high=max_mm, size=days)

    df = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "rainfall_mm": rainfall
    })

    df = df.sort_values("date")
    return df

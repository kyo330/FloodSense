import pandas as pd

def load_infrastructure_data(filepath="data/infrastructure.csv"):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return pd.DataFrame()

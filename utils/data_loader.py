import pandas as pd
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "car_data_expanded.csv"
)


def load_car_data():

    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()

    df = pd.read_csv(DATA_FILE)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    return df

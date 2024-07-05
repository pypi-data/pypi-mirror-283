import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path, index_col='Datetime', parse_dates=True)
    return df

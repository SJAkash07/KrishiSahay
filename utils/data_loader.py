import pandas as pd

def load_sheet(url):
    df = pd.read_csv(url)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

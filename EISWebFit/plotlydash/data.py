"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd


def create_dataframe(inputStr="data/File"):
    """Create Pandas DataFrame from local CSV."""

    print(inputStr)

    if inputStr == "Start" or inputStr is None:
        df = pd.DataFrame()
        df["f"] = [1]
        df["Re"] = [1]
        df["Im"] = [1]

    elif inputStr == "data/File" or inputStr == "File":
        df = pd.DataFrame()

    else:
        df = pd.read_csv(inputStr,sep="[\t ,]", engine='python')
        df.columns = ["f","Re","Im"]




    return df

import pandas as pd
import numpy as np
def gen_position(df: pd.DataFrame) -> pd.DataFrame:
    # Copy dữ liệu gốc
    df = df.copy()

    # Tính các chỉ số Moving Average
    MA_short = 10
    MA_long = 30
    df["MA_short"] = df["Close"].rolling(MA_short).mean()
    df["MA_long"] = df["Close"].rolling(MA_long).mean()

    # Tạo tín hiệu giao dịch
    df["position"] = 0 # Không hành động
    df.loc[df["MA_short"] > df["MA_long"], "position"] = 1   # Long
    df.loc[df["MA_short"] < df["MA_long"], "position"] = -1  # Short
    df["position"] = df["position"].fillna(0)

    return df
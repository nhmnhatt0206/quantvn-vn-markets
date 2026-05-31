# Khởi tạo client và import các module
import os
from dotenv import load_dotenv
load_dotenv()  # đọc .env vào Python
from quantvn import client
import pandas as pd
import numpy as np
from quantvn.vn.data import get_derivatives_hist
from quantvn.vn.metrics import Backtest_Derivates
client(apikey=os.getenv("QUANTVN_API_KEY"))

df = get_derivatives_hist("VN30F1M", "1m")
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

df_pos = gen_position(df)
print(df_pos)
backtest = Backtest_Derivates(df_pos, pnl_type="raw")
backtest.PNL()
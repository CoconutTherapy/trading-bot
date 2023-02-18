import pdb

import pandas as pd

from utils import data, binance, file


def test_signal():
    df = data.get_df("XRPUSDT-1m")

    df["middle_rolling"] = df["close"].rolling(15).mean()
    df["max"] = df["close"].rolling(15).max()
    df["middle_trend"] = df["middle_rolling"] - df["middle_rolling"].shift(1)
    df["drop"] = ((df["low"] / df["close"] - 1) < -0.02) & (df["middle_trend"] < 0)

    df = df[df["drop"]]

    df["dt"] = pd.to_datetime(df["open_time"], unit="ms")
    df["dt"] = df["dt"].apply(lambda x: x.strftime("%Y-%m-%d"))

    days = df["dt"].unique()

    for each in days:
        dt = pd.to_datetime(each)
        download_url = binance.get_download_url("XRPUSDT", "1s", date=dt)
        filename = binance.get_pair_filename("XRPUSDT", "1s", each, extension="zip")
        file.download_file(download_url, filename)
        file.unzip_file(filename)

    pdb.set_trace()


if __name__ == "__main__":
    test_signal()

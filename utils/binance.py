import pandas as pd


def get_download_url(pair, interval, date=None, month=None):
    dt = month.strftime("%Y-%m") if month else date.strftime("%Y-%m-%d")
    itr = "monthly" if month else "daily"

    filename = get_pair_filename(pair, interval, dt)

    return f"https://data.binance.vision/data/spot/{itr}/klines/{pair}/{interval}/{filename}"


def get_pair_filename(pair, interval, dt, extension="zip"):
    return f"{pair}-{interval}-{dt}.{extension}"


def df_from_files(files):
    headers = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ]

    dfs = []
    for f in files:
        df = pd.read_csv(f, names=headers)
        dfs.append(df)

    return pd.concat(dfs)

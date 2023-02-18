import pandas as pd

store = pd.HDFStore("store.h5")


def store_df(key, df):
    store[key] = df


def get_df(key):
    return store[key]

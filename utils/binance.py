import asyncio
from datetime import date

import settings
from utils.file import download_file, unzip_file
from utils.helpers import add_months
from utils.logs import logger


def get_download_url(pair, interval, date=None, month=None):
    dt = month.strftime("%Y-%m") if month else date.strftime("%Y-%m-%d")
    itr = "monthly" if month else "daily"

    filename = get_pair_filename(pair, interval, dt)

    return f"https://data.binance.vision/data/spot/{itr}/klines/{pair}/{interval}/{filename}"


def get_pair_filename(pair, interval, dt, extension="zip"):
    return f"{pair}-{interval}-{dt}.{extension}"


async def download_and_extract(pair, interval, dt):
    logger.info(f"Refreshing data for {pair} {interval} {dt}")
    url = get_download_url(pair, interval, month=dt)
    filename = get_pair_filename(pair, interval, dt.strftime("%Y-%m"))
    downloaded = await download_file(url, filename, False)
    if not downloaded:
        return
    await unzip_file(filename, False)


async def sync_pair_data(pair, interval, since):
    tasks = []
    logger.info(f"Syncing data for {pair} {interval} {since}")
    while since < date.today():
        tasks.append(download_and_extract(pair, interval, since))
        since = add_months(since, 1)
        if len(tasks) >= settings.MAX_CONCURRENT_DOWNLOADS or since >= date.today():
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks = []


CSV_HEADERS = [
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

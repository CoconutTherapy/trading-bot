import os
from datetime import date

import asyncclick as click

import settings
from utils import binance, file
from utils.enums import Interval
from utils.logs import logger


@click.group()
def cli():
    pass


@cli.command()
@click.option("--pair", "-p", help="Pair to download")
@click.option("--interval", "-i", default=Interval.MINUTE, help="Interval to download")
@click.option("--since", "-s", default=date(2018, 1, 1), help="Date of origin")
async def sync_pair(pair, interval=Interval.MINUTE, since=None):
    if not pair:
        click.echo("Please provide a pair")
        return
    since = date.fromisoformat(since)
    await binance.sync_pair_data(pair, interval, since)


@cli.command()
@click.option("--pair", "-p", help="Pair")
@click.option("--interval", "-i", default=Interval.MINUTE, help="Interval")
def merge_pair_files(pair, interval):
    files = [
        os.path.join(root, name)
        for root, dirs, files in os.walk(settings.csv_files_dir, topdown=False)
        for name in files
        if name.startswith(f"{pair}-{interval}")
    ]

    if not files:
        logger.info(f"No files found for {pair} {interval}")
        return

    target = settings.merged_files_dir / f"{pair}-{interval}.csv"
    logger.info(
        f'Merging {len(files)} files for {pair} {interval} into {settings.merged_files_dir / f"{pair}-{interval}.csv"}'
    )
    file.merge_files(files, target)


if __name__ == "__main__":
    cli(_anyio_backend="asyncio")

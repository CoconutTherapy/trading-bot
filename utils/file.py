import os
import zipfile

import requests

import settings
from utils.logs import logger


def merge_files(files, target):
    with open(settings.csv_files_dir / target, "w") as outfile:
        for fname in files:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    return target


def download_file(url, filename, force=False):
    fp = settings.raw_files_dir / filename
    if force or not os.path.exists(fp):
        logger.info(f"Downloading {filename}")
        with open(fp, "wb") as f:
            response = requests.get(url)
            f.write(response.content)

    return fp


def unzip_file(filename, force=False):
    target = settings.csv_files_dir / (filename.replace(".zip", ".csv"))
    try:
        if force or not os.path.exists(target):
            logger.info(f"Unzipping {filename}")
            with zipfile.ZipFile(settings.raw_files_dir / filename, "r") as zip_ref:
                zip_ref.extractall(settings.csv_files_dir)
    except zipfile.BadZipFile:
        logger.error(f"Bad zip file: {filename}")
        return None
    return target

__author__ = "PyPSA meets Earth"
__copyright__ = "Copyright 2022, The PyPSA meets Earth Initiative"
__license__ = "MIT"

"""Geofabrik Data Download

This module contains functions to download Geofabrik data.

"""


import os
import logging
from tqdm.auto import tqdm
import requests
import urllib3
import shutil
import hashlib


logger = logging.getLogger("osm_geo")
logger.setLevel(logging.INFO)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def earth_downloader(url, dir):
    """
    Download file from url to dir

    Args:
        url (str): url to download
        dir (str): directory to download to

    Returns:
        str: filepath of downloaded file
    """
    filename = os.path.basename(url)
    filepath = os.path.join(dir, filename)
    logger.info(f"{filename} downloading to {filepath}")
    os.makedirs(os.path.dirname(filepath), exist_ok=True) #  create download dir
    with requests.get(url, stream=True, verify=False) as r:
        if r.status_code == 200:
            # url properly found, thus execute as expected
            file_size = int(r.headers.get('Content-Length', 0))
            desc = "(Unknown total file size)" if file_size == 0 else ""
            with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc, leave=False) as raw:
                with open(filepath, "wb") as f:
                    shutil.copyfileobj(raw, f)
        else:
            # error status code: file not found
            logger.error(
                f"Error code: {r.status_code}. File {filename} not downloaded from {url}"
            )
            filepath = None
    return filepath


def download_pbf(url, update, data_dir):
    
    dir = os.path.join(data_dir, "pbf")
    pbf_filename = os.path.basename(url)
    pbf_filepath = os.path.join(dir, pbf_filename)

    # TODO: multi-part download each file for parallel downloading... (pip install pySmartDL)
    if not os.path.exists(pbf_filepath):
        # download file
        d_filepath = earth_downloader(url, dir)
        assert(d_filepath == pbf_filepath)
    else:
        logger.debug(f"{pbf_filename} already exists in {pbf_filepath}")

    return pbf_filepath


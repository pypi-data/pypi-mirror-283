#!/usr/bin/python3
import json
import logging
import os
from pathlib import Path
import requests

from deserializers import deserialize

S3_ENDPOINT = 'https://lnti-bigbeans-problems-dataset-public.s3.dualstack.us-east-2.amazonaws.com'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_key(problem_name):
    return problem_name + '/data.pkl'


def get_dest_file(problem_name, file_name, data_home=None) -> str:
    if data_home is None:
        data_home = str(Path.home()) + '/.bigbeans'
    return data_home + '/' + problem_name + '/' + file_name


def fetch_s3_file(problem_name, file_name, data_home=None):
    object_key = problem_name + '/' + file_name
    local_file = get_dest_file(problem_name, file_name, data_home)
    logger.debug(f"Downloading {object_key} to {local_file}")
    # make sure the directory exists
    local_dir = local_file[:local_file.rfind('/')]
    os.makedirs(local_dir, exist_ok=True)
    with open(local_file, 'wb') as f:
        f.write(requests.get(S3_ENDPOINT + '/' + object_key).content)
    return local_file


def fetch(problem_name, data_home=None):
    metadata_file = fetch_s3_file(problem_name, 'data.json', data_home)
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
        extension = metadata['format']
        fetched_file = fetch_s3_file(problem_name, 'data.bin', data_home)
        return deserialize(fetched_file, extension)

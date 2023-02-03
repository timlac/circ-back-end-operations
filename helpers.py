import logging
import re
from glob import glob
from pathlib import Path


def get_digits_only(mixed_string):
    """
    :param mixed_string: some string that may contain digits and characters
    :return: only digits
    """
    return re.sub("\\D", "", mixed_string)


def name2list(file_name):
    return file_name.split("_")


def get_filename(file_path):
    """
    :param file_path: some file path
    :return: filename without path or extension
    """
    return Path(file_path).stem


def get_file_paths(path):
    csv_paths = glob(path + '*.csv')
    logging.info("Files found:" + str(len(csv_paths)))
    return csv_paths

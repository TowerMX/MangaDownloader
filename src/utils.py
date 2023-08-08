import datetime
import pytz
from urllib.parse import urlparse
from pathlib import Path
from PIL import Image
import shutil
import os
from . import const


def convert_to_pdf(manga_name, temp_folder=const.DEFAULT_TEMP_FOLDER, save_folder=const.DEFAULT_SAVE_FOLDER):
    pass


def delete_images(manga_name, temp_folder=const.DEFAULT_TEMP_FOLDER):
    shutil.rmtree(rf"{temp_folder}\{manga_name}", ignore_errors=True)


def compare_times(time1, time2):
    # Time1 > Time2
    aux1 = time1.split(":")
    aux2 = time2.split(":")

    hour1 = int(aux1[0])
    hour2 = int(aux2[0])

    minute1 = int(aux1[1])
    minute2 = int(aux2[1])

    greater = False
    if hour1 >= hour2 and minute1 > minute2:
        greater = True
    return greater


def remove_dict_nones(dic):
    filtered_data = {k: v for k, v in dic.items() if v is not None}
    return filtered_data


def get_current_day_and_hour():
    # Get the current time in the local timezone
    local_time = datetime.datetime.now()

    # Set the timezone to GMT+1
    gmt_minus_1 = pytz.timezone("Etc/GMT-1")

    # Convert the local time to the GMT+1 timezone
    gmt_minus_1_time = local_time.astimezone(gmt_minus_1)

    numeric_weekday = gmt_minus_1_time.today().weekday()
    time = gmt_minus_1_time.time()
    parsed_time = f"{str(time.hour).zfill(2)}:{str(time.minute).zfill(2)}"
    return const.WEEK_DAYS[numeric_weekday], parsed_time


def extract_time_from_query(full_url):
    parsed_url = urlparse(full_url)
    full_query = parsed_url.query
    time = full_query.split("=")[1]
    return int(time)


def extract_rel_url_with_query(full_url):
    parsed_url = urlparse(full_url)
    path = parsed_url.path
    query = parsed_url.query

    relative_path = f"{path}?{query}"
    return relative_path

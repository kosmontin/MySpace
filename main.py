import os
import random
import time
from _datetime import datetime
from urllib.parse import urlparse

import requests
import telegram
from dotenv import load_dotenv


def get_imagefile_paths(folder='images'):
    filepaths = []
    for dirpath, dirnames, filenames in os.walk(folder):
        filepaths.extend(os.path.join(dirpath, filename) for filename in filenames if filename.endswith(
            ('.jpeg', '.jpg', '.png', '.gif')))
    return filepaths


def send_img_to_channel(api_key, chat_id, filepath):
    bot = telegram.Bot(token=api_key)
    with open(filepath, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)


def get_file_extension(url):
    extension = os.path.splitext(os.path.basename(urlparse(url).path))[-1]
    return extension


def download_image(url, path, params=None):
    filename = os.path.basename(urlparse(url).path)
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(os.path.join(path, filename), 'wb') as file:
        file.write(response.content)


def fetch_nasa_epic(api_key):
    most_recent_date_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    filespath = os.path.join('images', 'NASA', 'EPIC')
    params = {
        'api_key': api_key
    }

    response = requests.get(most_recent_date_url, params=params)
    response.raise_for_status()
    dates_info = response.json()
    date = datetime.strptime(dates_info[0]['date'], '%Y-%m-%d %H:%M:%S').date()

    photos_info_per_day_url = f'https://api.nasa.gov/EPIC/api/natural/date/{date.strftime("%Y-%m-%d")}'
    response = requests.get(photos_info_per_day_url, params=params)
    response.raise_for_status()
    photos_info = response.json()
    os.makedirs(filespath, exist_ok=True)
    for photo in photos_info:
        earth_photo_url = \
            f'https://api.nasa.gov/EPIC/archive/natural/{date.strftime("%Y/%m/%d")}/png/{photo["image"]}.png'
        download_image(earth_photo_url, filespath, params)


def fetch_nasa_apod(api_key):
    filespath = os.path.join('images', 'NASA', 'APOD')
    params = {
        'api_key': api_key,
        'count': 30
    }
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()
    photos = response.json()
    os.makedirs(filespath, exist_ok=True)
    for photo in photos:
        download_image(photo['url'], filespath, params={'api_key': api_key})


def fetch_spacex_last_launch():
    filespath = 'images'
    params = {
        'launch_year': 2020,
        'limit': 10
    }
    response = requests.get('https://api.spacexdata.com/v3/launches/', params=params)
    response.raise_for_status()
    flights = response.json()
    flight_urls = []
    if flights:
        os.makedirs(filespath, exist_ok=True)
        for flight in flights:
            flight_urls.extend(flight['links']['flickr_images'])
        for url in flight_urls:
            download_image(url, filespath)


def main():
    load_dotenv()
    delay = os.getenv('SEND_DELAY', 86400)
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    telegram_api_key = os.getenv('TELEGRAM_API_KEY')
    nasa_api_key = os.getenv('NASA_API_KEY')
    fetch_spacex_last_launch()
    fetch_nasa_apod(nasa_api_key)
    fetch_nasa_epic(nasa_api_key)
    filepaths = get_imagefile_paths()
    random.shuffle(filepaths)
    for filepath in filepaths:
        send_img_to_channel(telegram_api_key, telegram_chat_id, filepath)
        time.sleep(float(delay))


if __name__ == '__main__':
    main()

import os
import random
import time
from urllib.parse import urlparse, urlencode

import requests
import telegram
from dotenv import load_dotenv


def get_filepaths(folder='images'):
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


def download_image(url, path='images'):
    filename = os.path.basename(urlparse(url).path)
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), 'wb') as file:
        file.write(response.content)


def fetch_nasa_epic(api_key):
    files_per_day = 'https://api.nasa.gov/EPIC/api/natural/date/2022-02-12'
    params = {
        'api_key': api_key
    }
    response = requests.get(files_per_day, params=params)
    response.raise_for_status()
    photos_info = response.json()
    photo_ids = []
    for photo in photos_info:
        photo_ids.append(photo['image'])

    for photo_id in photo_ids:
        earth_photo_url = f'https://api.nasa.gov/EPIC/archive/natural/2022/02/12/png/{photo_id}.png?{urlencode(params)}'
        download_image(earth_photo_url, 'images\\NASA\\EPIC')


def fetch_nasa_apod(api_key):
    params = {
        'api_key': api_key,
        'count': 30
    }
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()
    photos = response.json()
    for photo in photos:
        download_image(photo['url'], 'images\\NASA\\APOD')


def fetch_spacex_last_launch():
    params = {
        'launch_year': 2020,
        'limit': 10
    }
    response = requests.get('https://api.spacexdata.com/v3/launches/', params=params)
    response.raise_for_status()
    flights = response.json()
    flight_urls = []
    if flights:
        for flight in flights:
            flight_urls.extend(flight['links']['flickr_images'])
        for url in flight_urls:
            download_image(url)


def main():
    load_dotenv()
    delay = os.getenv('SEND_DELAY', 86400)
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    telegram_api_key = os.getenv('TELEGRAM_API_KEY')
    nasa_api_key = os.getenv('NASA_API_KEY')
    fetch_spacex_last_launch()
    fetch_nasa_apod(nasa_api_key)
    fetch_nasa_epic(nasa_api_key)
    filepaths = get_filepaths()
    random.shuffle(filepaths)
    for filepath in filepaths:
        send_img_to_channel(telegram_api_key, telegram_chat_id, filepath)
        time.sleep(float(delay))


if __name__ == '__main__':
    main()

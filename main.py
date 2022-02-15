import os
from urllib.parse import urlparse, urlencode

import requests
import telegram
from dotenv import load_dotenv


def get_filepaths(folder='images'):
    filepaths = []
    for dirpath, dirnames, filenames in os.walk(folder):
        filepaths.extend(os.path.join(dirpath, filename) for filename in filenames)
    return filepaths


def send_img_to_channel(filepath):
    load_dotenv()
    api_key = os.getenv('TELEGRAM_API_KEY')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(token=api_key)
    bot.send_document(chat_id=chat_id, document=open(filepath, 'rb'))


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


def fetch_spacex_last_launch():
    params = {
        'launch_year': 2020,
        'limit': 3
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
    api_key = os.getenv('NASA_API_KEY')
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
        download_image(earth_photo_url, 'images\\EARTH')


if __name__ == '__main__':
    main()

import os
from urllib.parse import urlparse

import requests


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
    params = {
        'api_key': 'DEMO_KEY',  # TODO: Add using .env via dotenv
        'count': 30
    }
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()
    photos = response.json()
    for photo in photos:
        download_image(photo['url'], 'images\\NASA')


if __name__ == '__main__':
    main()

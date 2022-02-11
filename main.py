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
    url = 'https://example.com/txt/hello%20world.txt?v=9#python'
    print(get_file_extension(url))


if __name__ == '__main__':
    main()

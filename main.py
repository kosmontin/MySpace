import os

import requests


def download_image(url, path='images'):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'hubble.jpeg'), 'wb') as file:
        file.write(response.content)


def main():
    download_image('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg')
    params = {
        'launch_year': 2020,
        'limit': 3
    }
    response = requests.get('https://api.spacexdata.com/v3/launches/', params=params)
    response.raise_for_status()
    flights = response.json()
    if flights:
        for flight in flights:
            print(*flight['links']['flickr_images'], sep='\n')


if __name__ == '__main__':
    main()

import os

import requests

images_dir = 'images'
response = requests.get('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg')
os.makedirs(images_dir, exist_ok=True)
with open(os.path.join(images_dir, 'hubble.jpeg'), 'wb') as file:
    file.write(response.content)

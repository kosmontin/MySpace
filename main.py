import requests

response = requests.get('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg')
with open('hubble.jpeg', 'wb') as file:
    file.write(response.content)

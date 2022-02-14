import os

import telegram
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('TELEGRAM_API_KEY')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

text_speech = 'Hello, my friend. My name is Dormammu. Would you talk with me?'
bot = telegram.Bot(token=API_KEY)
# bot.send_message(text=text_speech, chat_id=CHAT_ID)
bot.send_document(chat_id=CHAT_ID, document=open('images/NASA/skylab_nasa.jpg', 'rb'))

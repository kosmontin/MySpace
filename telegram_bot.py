import telegram

API_KEY = ''
CHAT_ID = 258213590

text_speech = 'Hello, my friend. My name is Dormammu. Would you talk with me?'
bot = telegram.Bot(token=API_KEY)
bot.send_message(text=text_speech, chat_id=CHAT_ID)

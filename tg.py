import telebot
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
translator = Translator()
from pymongo import MongoClient

cluster = MongoClient("mongodb://zazikbot:dtgDT9x9HHAoZwuP@cluster0-shard-00-00.4teix.mongodb.net:27017,cluster0-shard-00-01.4teix.mongodb.net:27017,cluster0-shard-00-02.4teix.mongodb.net:27017/db?ssl=true&replicaSet=atlas-46qpsn-shard-0&authSource=admin&retryWrites=true&w=majority")
db=cluster["db"]
collection=db["user_info"]


TOKEN = '1415859615:AAG7VHsj3pOoy0XHo07lUTPeerC2xf7Lkes'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
  reg=collection.find_one({"_id": message.chat.id})
  if reg == None:
    collection.insert_one({"_id":message.chat.id})
    bot.send_message(message.chat.id, "🎃 В каком городе ищем погоду?")
    bot.register_next_step_handler(message, poisk)
  else:
    bot.send_message(message.chat.id, "🎃 В каком городе ищем погоду?")
    bot.register_next_step_handler(message, poisk)

@bot.message_handler(func=lambda c:True)
def poisk(message):
  while(1):
    try:
      city= message.text.lower()
      print(city)
      headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
      respd = requests.get(f'https://sinoptik.com.by/погода-{city}', headers=headers, verify=False) 
      print(respd)
      soup = BeautifulSoup(respd.text, 'html.parser')
      title = soup.find('div', class_='weather__content_tab-temperature') 
      temperature = title.select_one('div', class_= 'min')
      temperature1 = temperature.select_one('b').text
      temperature2 = title.select('b')[1].text
      
      bot.send_message(message.chat.id, f'Мин: {str(temperature1)}\nМакс: {str(temperature2)}')
      break
    except Exception:
      bot.send_message(message.chat.id, 'Неверно указан город или указывайте на русском!')
      break
bot.polling()
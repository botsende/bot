from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import telebot # pip install pyTelegramBotApi
from telebot import types
import googletrans
from googletrans import Translator

lang = "ru"

translator = Translator()
# ---------- FREE API KEY examples ---------------------
bot = telebot.TeleBot('1403575560:AAHUlgnESfLpZIYGxau0p8rTKuiPzPceHZY', parse_mode=None)
owm = OWM('a03787689fc0bc4027b0061ce6391dbd')
mgr = owm.weather_manager()



@bot.message_handler(commands=["start"])
def inline(message):
    bot.send_message(message.chat.id, "🎃 Выбери язык\n/ru - русский\n/en - english" )
    

@bot.message_handler(commands=["ru"])
def inline(message):
    global lang
    bot.send_message(message.chat.id, "🎃 Вы выбрали русский язык, теперь пишите город" )
    lang = "ru"


@bot.message_handler(commands=["en"])
def inline(message):
    global lang
    bot.send_message(message.chat.id, "🎃 You have chosen English, now write city" )
    lang = "en"
    
    
@bot.message_handler(func=lambda m: True)
def echo_all(message):
  
  while(1):
    try:
      if lang == "ru":
        print(lang)
        city=message.text
        observation = mgr.weather_at_place(city)
        w = observation.weather
        temperature = w.temperature('celsius')["temp"]
        detailed = w.detailed_status
        result = translator.translate(detailed, dest='ru')
        bot.send_message(message.chat.id, "🌐"+city+":\n"+"  Температура = "+str(temperature)+"С⁰\n"+"  Тип: "+str(result.text))
        break
      else:
        city=message.text
        observation = mgr.weather_at_place(city)
        w = observation.weather
        temperature = w.temperature('celsius')["temp"]
        detailed = w.detailed_status
        bot.send_message(message.chat.id, "🌐"+city+":\n"+"  Temperature = "+str(temperature)+"С⁰\n"+"  Type: "+str(detailed))
        break
    except Exception:
      if lang == "ru":
        bot.send_message(message.chat.id, "Неверно указан город!")
        break
      else:
        bot.send_message(message.chat.id, "City is incorrect!")
        break
  
bot.polling()

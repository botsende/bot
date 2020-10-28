from pymongo import MongoClient
from random import randint
import random
import vk_api
from datetime import datetime,date

cluster = MongoClient("mongodb://zazikbot:CmKrjqSmOsFwKkeY@cluster0-shard-00-00.4teix.mongodb.net:27017,cluster0-shard-00-01.4teix.mongodb.net:27017,cluster0-shard-00-02.4teix.mongodb.net:27017/db?ssl=true&replicaSet=atlas-46qpsn-shard-0&authSource=admin&retryWrites=true&w=majority")
db=cluster["db"]
collection=db["user_info"]

from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token="115dee4d1a05e66bc577c36c826ac2b3f19b79e8759256f82177a7bd42db28cfeff5555b0d209f48ddb12")

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()



global Random

def random_id():
    Random = 0
    Random += random.randint(0, 1000000000);
    return Random
    
while True:
  for event in longpoll.listen():
      if event.type == VkEventType.MESSAGE_NEW and event.to_me:

          if event.text.lower() == "начать":
            user_id=event.user_id,
            result = collection.find_one({"_id":event.user_id})
            if result != None:
                vk.messages.send(
                  user_id=event.user_id,
                  message="Вы уже зарегестрированы!",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())
                      
            else:
                 standartnick="Ник"
                 collection.insert_one({"_id":event.user_id, "name":standartnick, "balance": 100, "bdate":0, "status":0})
                 vk.messages.send(
                   user_id=event.user_id,
                   message="Вы успешно зарегестрированы!",
                   keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                   random_id=random_id())
    
        
          elif event.text.lower()[0:8] == "передать":
            reg=collection.find_one({"_id":event.user_id})
            print(reg)
            if reg != None:
              stroka=event.text.split()
              if len(stroka) == 3:
                idp=int(event.text.split()[1])
                summa=int(event.text.split()[2])
                idp2=collection.find_one({"_id": idp})
                nickp=collection.find_one({"_id":idp})["name"]
                if summa > 0:
                  if idp2 != None:
                    balance=collection.find_one({"_id":event.user_id})["balance"]
                    if balance >= summa:
                      balancep=collection.find_one({"_id":idp})["balance"]
                      collection.update_one({"_id":idp}, {"$set": {"balance": balancep + summa}})
                      balance=collection.find_one({"_id":event.user_id})["balance"]
                      collection.update_one({"_id":event.user_id}, {"$set": {"balance":balance - summa}})
                      balance=collection.find_one({"_id":event.user_id})["balance"]
                      vk.messages.send(
                        user_id=event.user_id,
                        message=f"✅Вы успешно передали: {summa}$\nПользователю: {nickp}\nВаш баланс: {balance}$",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id())
                    else:
                      vk.messages.send(
                        user_id=event.user_id,
                        message="❌Вы ввели число больше вашего баланса!",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id())
                            
                  else:
                    vk.messages.send(
                      user_id=event.user_id,
                      message="❌Юзера с таким id не найдено!",
                      keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                      random_id=random_id()) 
                else:
                  vk.messages.send(
                      user_id=event.user_id,
                      message="❌Неверная сумма введена!",
                      keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                      random_id=random_id()) 
            else:
              vk.messages.send(
                  user_id=event.user_id,
                  message=f"Вы ещё не зарегистрированы!\n Напишите 'Начать', что бы зарегистрироваться!",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())        
                    
          elif event.text.lower() == "профиль":
            log = collection.find_one({"_id": event.user_id})
            if log != None:
              idpolz=collection.find_one({"_id":event.user_id})["_id"]
              balpolz=collection.find_one({"_id":event.user_id})["balance"]
              status=collection.find_one({"_id":event.user_id})["status"]
              if status == 0:
                nick=collection.find_one({"_id":event.user_id})["name"]
                vk.messages.send(
                  user_id=event.user_id,
                  message=f"{nick}, ваш профиль:\n🔎ID: {idpolz}\n🌀Ваш статус: Игрок\n💸Баланс: {balpolz}$",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())
              else:
                nick=collection.find_one({"_id":event.user_id})["name"]
                vk.messages.send(
                  user_id=event.user_id,
                  message=f"{nick}, ваш профиль:\n🔎ID: {idpolz}\n🌀Ваш статус: Админ👑\n💸Баланс: {balpolz}$",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())
            else:
              vk.messages.send(
                  user_id=event.user_id,
                  message=f"Вы ещё не зарегистрированы!\n Напишите 'Начать', что бы зарегистрироваться!",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())
          elif event.text.lower() == "правила":
            vk.messages.send(
                  user_id=event.user_id,
                  message=f"🧠Всеправила указаны в данной статье↓\nvk.com/@botzazik-vse-pravila-bota-bot-zazik",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())
          
          elif event.text.lower()[0:6] == "казино":
            log = collection.find_one({"_id": event.user_id})
            if log != None:
              stroka=event.text.split()
              if len(stroka) == 2:
                  balance1 = collection.find_one({"_id":event.user_id})["balance"]
                  print(balance1)
                  stavka = (event.text.split()[1])
                  
                  if stavka.isdigit():
                    stavka2 = int(stavka)
                    if balance1 >= stavka2:
                      randcas = random.randint(1,2)
                      if randcas == 1:
                        collection.update_one({"_id": event.user_id}, {"$set": {"balance": balance1 + stavka2}})
                        balance1=collection.find_one({"_id": event.user_id})["balance"]
                        vk.messages.send(
                            user_id=event.user_id,
                            message=f"✔️Вы выиграли!\nВаш баланс теперь:{balance1}$😄",
                            keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                            random_id=random_id())
                      else:
                        collection.update_one({"_id":event.user_id}, {"$set": {"balance": balance1 - stavka2}})
                        balance1=collection.find_one({"_id":event.user_id})["balance"]
                        vk.messages.send(
                              user_id=event.user_id,
                              message=f"❌Вы програли!\nВаш баланс теперь:{balance1}$😔",                              keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                            random_id=random_id())
                    else:
                             vk.messages.send(
                             user_id=event.user_id,
                             message="Вы указали ставку больше вашего баланса!",
                             random_id=random_id())
                  else:
                           vk.messages.send(
                             user_id=event.user_id,
                             message="Вы неверно указали ставку!",
                             random_id=random_id())         
            else:
              vk.messages.send(
                  user_id=event.user_id,
                  message=f"Вы ещё не зарегистрированы!\n Напишите 'Начать', что бы зарегистрироваться!",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())
                  
          elif event.text.lower() == "бонус":
            log = collection.find_one({"_id": event.user_id})
            if log != None:
              date1=date.today()
              date2=collection.find_one({"_id":event.user_id})["bdate"]
              date3=date1.day
              date4=date2
              if date3 != date4:
                collection.update_one({"_id": event.user_id}, {"$set": {"bdate":date3}})
                bonus=random.randint(1,100000)
                collection.update_one({"_id":event.user_id}, {"$set": {"balance": bonus}})
                vk.messages.send(
                    user_id=event.user_id,
                    message=f"Бонус успешно снят!\nВам выпало: {bonus}$💶",
                    random_id=random_id())
              else:
                  vk.messages.send(
                  user_id=event.user_id,
                  message="Бонус уже снят!\nПриходите в 0:00 за новым бонусом!💷",
                                  random_id=random_id())
                            
            else:
              vk.messages.send(
                  user_id=event.user_id,
                  message=f"Вы ещё не зарегистрированы!\n Напишите 'Начать', что бы зарегистрироваться!",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())
          elif event.text.lower()[0:6] == "выдать":
            
            reg=collection.find_one({"_id":event.user_id})
            print(reg)
            if reg != None:
              status=collection.find_one({"_id":event.user_id})["status"]
              if status == 1:
                stroka=event.text.split()
                if len(stroka) == 3:
                  _id=int(event.text.split()[1])
                  status=int(event.text.split()[2])
                  _id2=collection.find_one({"_id": _id})
                  if _id2 != None:
                    
                      
                      collection.update_one({"_id":_id}, {"$set": {"status": status}})
                      statusp=collection.find_one({"_id":_id})["status"]
                      
                      vk.messages.send(
                        user_id=event.user_id,
                        message=f"Вы успешно выдали статус: {statusp} пользователю: {_id}💥",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id())
                    
                  else:
                    vk.messages.send(
                      user_id=event.user_id,
                      message="❌Юзера с таким id не найдено!",
                      keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                      random_id=random_id()) 
              else:
                vk.messages.send(
                      user_id=event.user_id,
                      message="❌У вас статус ниже Admin!",
                      keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                      random_id=random_id()) 
            else:
              vk.messages.send(
                  user_id=event.user_id,
                  message=f"Вы ещё не зарегистрированы!\n Напишите 'Начать', что бы зарегистрироваться!",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())    
                  
          elif event.text.lower()[0:3]== "ник":
            reg=collection.find_one({"_id":event.user_id})
            print(reg)
            if reg != None:
              stroka=event.text.split()
              if len(stroka) == 2:
                nick=event.text.split()[1]
                print(nick)
                collection.update_one({"_id":event.user_id}, {"$set": {"name": nick}})
                vk.messages.send(
                  user_id=event.user_id,
                  message=f"Ник успешно сменен на: {nick}!👍",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())  
              else:
                vk.messages.send(
                  user_id=event.user_id,
                  message=f"Вы не указали ник либо допустили ошибку!(ник должен быть в 1 слово!)",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())    
                
            else:
              vk.messages.send(
                  user_id=event.user_id,
                  message=f"Вы ещё не зарегистрированы!\n Напишите 'Начать', что бы зарегистрироваться!",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())    
        
        
        
        
        
        
          
          else:
            vk.messages.send(
              user_id=event.user_id,
              message="Команда не найдена!",
              keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
              random_id=random_id())
          
          
          
        
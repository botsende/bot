import vk_api, random
import sqlite3
import casino
import peremen
from datetime import datetime,date

from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token="7d52fabe1fc3eba4bdcf40f0a6f346345d72d0f02490712b01973cb6beaa966db1cec650fee0146b55c8f")

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

conn = sqlite3.connect("db.db")
c = conn.cursor()

global Random


def random_id():
    Random = 0
    Random += random.randint(0, 1000000000);
    return Random


def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True


def update_balance(balance, user_id):
    c.execute("""UPDATE user_info SET balance = ? WHERE  user_id = ?""",(balance, user_id ))
    conn.commit()
    
def update_bonus(bonus, user_id):
    c.execute("""UPDATE user_info SET bonus = ? WHERE  user_id = ?""",(bonus, user_id ))
    conn.commit()
    
def update_bdate(bdate, user_id):
    c.execute("""UPDATE user_info SET bdate = ? WHERE user_id = ?""",(bdate, user_id ))
    conn.commit()
    
def plusbalance(balance, user_id):
    c.execute("""UPDATE user_info SET balance = balance + ? WHERE  user_id = ?""",(plus, user_id ))
    conn.commit()
  


 
def register_new_user(user_id):
    c.execute("INSERT INTO users(user_id, state) VALUES (%d, '')" % user_id)
    conn.commit()
    c.execute("INSERT INTO user_info(user_id, user_wish) VALUES (%d, 0)" % user_id)
    conn.commit()


def get_user_state(user_id):
    c.execute("SELECT state FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]

def nick(name, user_id):
    c.execute("""UPDATE user_info SET name = ? WHERE user_id = ?""", (peremen.da, user_id ))
    conn.commit()

def get_user_wish(user_id):
    c.execute("SELECT user_wish FROM user_info WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


def set_user_wish(user_id, user_wish):
    c.execute("UPDATE user_info SET user_wish = %d WHERE user_id = %d" % (user_wish, user_id))
    conn.commit()



while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            if not check_if_exists(event.user_id):
                register_new_user(event.user_id)
 
            if event.text.lower() == "правила":
                vk.messages.send(
                    user_id=event.user_id,
                    message="Все правила указаны в статье:\nvk.com/@botzazik-vse-pravila-bota-bot-zazik",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )

            elif event.text.lower() == "начать":
                if get_user_wish(event.user_id) == 0:
                  user_id=event.user_id,
                  nick(peremen.da, event.user_id)
                  
                  update_balance(100,event.user_id)
                  set_user_wish(event.user_id, 1)
                  vk.messages.send(
                        user_id=event.user_id,
                        message="Вы успешно зарегестрировались!\n можем начать, на ваш счёт зачислено 100$, пиши баланс",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random_id()
                        )
                
            elif event.text.lower() == "баланс":
                if get_user_wish(event.user_id) == 1:
                       user_id=event.user_id,
                       c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                       balance1 = c.fetchone()
                       vk.messages.send( 
                       user_id=event.user_id,
                     
                       message=f"Ваш баланс: {balance1[0]}$",
                       keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                       random_id=random_id())
                     
            elif event.text.lower()[0:4] == "плюс":
                 if get_user_wish(event.user_id) == 1:
                  stroka=event.text.split()
                  if len(stroka) == 2:
                    user_id=event.user_id,
                    c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                    balance1 = c.fetchone()
                    
                    plus = int(event.text.split()[1])
                    if plus >= 0:
                      user_id=event.user_id,
                      c.execute("""SELECT admin FROM user_info WHERE user_id = ? """, (user_id))
                      admins = c.fetchone()
                      print(admins[0])
                      if admins[0] == 1:
                        user_id=event.user_id,
                        c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                        balance1 = c.fetchone()
                        user_id=event.user_id,
                      
                        plusbalance(plus, event.user_id)
                        user_id=event.user_id,
                        c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                        balance1 = c.fetchone()
                        vk.messages.send(
                        user_id=event.user_id,
                        message=f"Успешно начислено!\nТеперь ваш баланс: {balance1[0]}$🤑",
                        random_id=random_id())
                    else:
                      vk.messages.send(
                        user_id=event.user_id,
                        message="Вы ввели отрицательное число!",
                        random_id=random_id())
            
            
                      
            elif event.text.lower() == "профиль":
                if get_user_wish(event.user_id) == 1:
                      user_id=event.user_id,
                      c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                      balance1 = c.fetchone()
                       
                      c.execute("""SELECT name FROM user_info WHERE user_id = ? """, (user_id))
                      nick2 = c.fetchone()
                      
                      c.execute("""SELECT user_id FROM users WHERE user_id = ? """, (user_id))
                      users_id = c.fetchone()
                         
                      user_id=event.user_id,
                      c.execute("""SELECT admin FROM user_info WHERE user_id = ? """, (user_id))
                      status = c.fetchone()
                      if status[0] == 1:
                        status1 = "Вип👑"
                        vk.messages.send(
                          user_id=event.user_id,
                          message=f"{nick2[0]}, твой профиль:\n🔎ID: {users_id[0]}\n🌀Твой статус: {status1}\n💰Баланс: {balance1[0]}$",
                          keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                          random_id=random_id()
                           )
                      else:
                        status1 = "Игрок👍"
                        vk.messages.send(
                          user_id=event.user_id,
                          message=f"{nick2[0]}, твой профиль:\n🔎ID: {users_id[0]}\n🌀Твой статус: {status1}\n💰Баланс: {balance1[0]}$",
                          keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                          random_id=random_id()
                          )
            elif event.text.lower()[0:6] == "казино":
                if get_user_wish(event.user_id) == 1:
                  stroka=event.text.split()
                  if len(stroka) == 2:
                    
                      user_id=event.user_id,
                      c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                      balance1 = c.fetchone()
                      stavka= (event.text.split()[1])
                      if stavka.isdigit():
                        user_id=event.user_id,
                        c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                        balance1 = c.fetchone()
                        print(balance1)
                        print(stavka)
                        stavka2 = int(stavka)
                        if balance1[0] >= stavka2:
                          randcas = casino.casino()
                          if randcas == 1:
                            
                            user_id=event.user_id,
                            c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                            balance1 = c.fetchone()
                            user_id=event.user_id,
                            update_balance(balance1[0] + stavka2, event.user_id)
                            c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                            balance1 = c.fetchone()
                            vk.messages.send(
                              user_id=event.user_id,
                              message=f"✔️Вы выиграли!\nВаш баланс теперь:{balance1[0]}$😄",
                              keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                            random_id=random_id())
                          else:
                              user_id=event.user_id,
                              c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                              balance1 = c.fetchone()
                              user_id=event.user_id,
                              update_balance(balance1[0] - stavka2,   event.user_id)
                              c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                              balance1 = c.fetchone()
                              vk.messages.send(
                                user_id=event.user_id,
                                message=f"❌Проигрыш!\nВаш баланс теперь: {balance1[0]}$😔",
                                keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                            random_id=random_id())
                      else:
                           vk.messages.send(
                             user_id=event.user_id,
                             message="Вы неверно указали ставку!",
                             random_id=random_id())
            
                                
            elif event.text.lower()[0:5] == "кубик": 
                if get_user_wish(event.user_id) == 1:
                  stroka=event.text.split()
                  if len(stroka) == 3:
                    
                      user_id=event.user_id,
                      c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                      balance1 = c.fetchone()
                      vibkub= int(event.text.split()[1])
                      stavka= int(event.text.split()[2])
                      print(balance1)
                      print(stavka)
                      
                      if balance1[0] >= stavka:
                        randkub = casino.kub()
                        if vibkub == randkub:
                            
                            user_id=event.user_id,
                            c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                            balance1 = c.fetchone()
                            user_id=event.user_id,
                            update_balance(balance1[0] + stavka, event.user_id)
                            vk.messages.send(
                              user_id=event.user_id,
                              message=f"Верно!",
                              keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                            random_id=random_id())
                        else:
                              user_id=event.user_id,
                              c.execute("""SELECT balance FROM user_info WHERE user_id = ? """, (user_id))
                              balance1 = c.fetchone()
                              user_id=event.user_id,
                              update_balance(balance1[0] - stavka,   event.user_id)
                              vk.messages.send(
                                user_id=event.user_id,
                                message=f"Проигрыш!\nЧислом было: {randkub}",
                                keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                            random_id=random_id())
           
                                
                      else:
                        vk.messages.send(
                          user_id=event.user_id,
                          message="Вам не хватает денег!",
                          keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                      random_id=random_id())
            
                  else:
                    vk.messages.send(
                      user_id=event.user_id,
                      message="Вы не указали либо число либо ставку!",
                      keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id())
                else:
                  vk.messages.send(
                    user_id=event.user_id,
                    message="Напиши 'Старт' для регистрации в боте",
                    random_id=random_id()
                            ) 
            elif event.text.lower() == "бонус":
                            date1 = date.today()
                            user_id=event.user_id,
                            c.execute("""SELECT bdate FROM user_info WHERE user_id = ? """, (user_id    ))
                            date2 = c.fetchone()
                            date3 = date1.day
                            date4 = date2[0]
                            if date3 != date4:
                              update_bdate(date3, event.user_id)
                              user_id=event.user_id,
                              update_bonus(0, event.user_id)
                              
                              c.execute("""SELECT bonus FROM user_info WHERE user_id = ? """, (user_id))
                              bonus = c.fetchone()
                              print(bonus[0])
                              if bonus[0] == 0:
                                 
                                bonusr=casino.bonus()
                                update_balance(bonusr, event.user_id)
                                user_id=event.user_id,
                                update_bonus(1, event.user_id )
                            
                                vk.messages.send(
                                  user_id=event.user_id,
                                  message=f"Бонус успешно снят!\nВам выпало: {bonusr}$",
                                  random_id=random_id())
                              else:
                                vk.messages.send(
                                  user_id=event.user_id,
                                  message="Бонус уже снят!",
                                  random_id=random_id())
                            else:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Вы уже забирали бонус, приходите в 0:00!",
                                    random_id=random_id())
            else:
                vk.messages.send(
                  user_id=event.user_id,
                  message="Нет такой команды!",
                  keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                  random_id=random_id()
                        )
                         
    
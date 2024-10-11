"""Бот для определения температуры для по городу"""

from telebot import TeleBot
import requests
import os
from translate import Translator
from dotenv import load_dotenv

load_dotenv()# Загрузка env-ов

translator = Translator(to_lang="en")

BOT_API_KEY = os.getenv('BOT_API_KEY')
WHETHER_URL = os.getenv('WHETHER_URL') # Это чтобы на git не выгружать
WHETHER_API_KEY = os.getenv('WHETHER_API_KEY')

bot = TeleBot(token=BOT_API_KEY)


def get_city(city_name: str) -> str: # начал ставить типизацию просто по тихой на го начинаю кодить и привыкаю)
    """Принемает название города.
     на английском и делает GET запрос на WHETHER_URL"""

    params = {
        'q': city_name,
        'appid': WHETHER_API_KEY,
        'units': 'metric'
    }

    response = requests.get(WHETHER_URL, params=params) # Сам GET запрос с parms(фильтрация грубо говоря)

    if response.status_code == 200: # В случае, если ответ 200, то вытягиваем и возвращаем резултьтаты
        data = response.json()
        main = data['main']
        wind = data['wind']
        temp = main['temp']
        humidity = main['humidity']
        wind_speed = wind['speed']
        return True, (f"Город {city_name}\n"
                f"Температура: {temp}°C\n"
                f"Скорость ветра: {wind_speed}м/с\n"
                f"Влажность:{humidity}%\n")

    elif response.status_code == 400 or response.status_code == 404: # bad request или Not found
        return False, "Данный город не найден"

    return False, "Данный сервис пока что не доступен. Попробуйте позже" # Если сервак откинул 500


@bot.message_handler(commands=['start'])
def start(message):
    """Ну обработка команды start.
    Возвращает сообщение
    """
    return bot.send_message(message.chat.id, "👋Привет.\n"
                                             "Я помогу тебе посмотреть погоду в товое городе.\n"
                                             "Просто введи название.\n"
                                             "По типу: Москва. "
                                             "Бот напсиан Скакун Дмитрием для тестового задания")


@bot.message_handler(func=lambda message: True)
def message(message):
    """Принемает message(предположительно название города).
    Возвращает сообщение пользователю
    """
    status, answer = get_city(message.text)
    return bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    bot.polling()
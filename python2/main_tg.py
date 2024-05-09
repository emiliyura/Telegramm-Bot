import requests
import datetime
from config import tg_bot_token, open_weather_token
from config import code_to_smile as code_to_smile
from config import code_to_clothes as code_to_clothes
import telebot
import random

bot = telebot.TeleBot(tg_bot_token)

@bot.message_handler(commands=["start"])
def start_command(message):
    bot.reply_to(message, "Привет! Напиши город.")

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        humidity = data["main"]["humidity"]
        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "Посмотри че там сам")
        current_weather = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]
        is_raining = "rain" in weather_description.lower()

        # Determine clothing advice based on temperature range
        if current_weather < -15:
            clothes_advice = code_to_clothes["cold"]
            wind_status = "windy" if wind_speed > 5 else "no_wind"
        elif current_weather < 0:
            clothes_advice = code_to_clothes["cold"]
            wind_status = "windy" if wind_speed > 3 else "no_wind"
        elif current_weather < 15:
            clothes_advice = code_to_clothes["moderate"]
            rain_status = "rainy" if is_raining else "no_rain"
        elif current_weather < 25:
            clothes_advice = code_to_clothes["warm"]
            wind_status = "windy" if wind_speed > 5 else "no_wind"
        else:
            clothes_advice = code_to_clothes["hot"]

        # Compose clothing advice
        advice = (
            f"~~~{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}~~~\n"
            f"Погода в городе: {city}\n\n"
            f"Температура: {current_weather} °C {wd}\n"
            f"Ветер: {wind_speed}\n"
            f"Влажность: {humidity}%\n\n"
            
            f"Советы по одежде:\n"
            f"{random.choice(clothes_advice[rain_status or wind_status or 'advice'])}"
        )

        bot.send_message(message.chat.id, advice)
    except Exception as e:
        print(f"Error occurred: {e}")
        bot.reply_to(message, "Проверьте название города")

if __name__ == '__main__':
    bot.polling(none_stop=True)


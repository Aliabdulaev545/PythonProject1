import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError('API_KEY не найден в .env')


def get_coords(city: str) -> tuple:
    '''Получение координат по названию города'''
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if not data:
        raise ValueError(f'Город "{city}" не найден')

    return data[0]['lat'], data[0]['lon']


def get_weather(lat: float, lon: float) -> dict:
    '''Получение погоды по координатам'''
    url = (
        f'http://api.openweathermap.org/data/2.5/weather'
        f'?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ru'
    )
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    lat, lon = get_coords('Moscow')
    weather = get_weather(lat, lon)
    print(weather)
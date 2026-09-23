import os
import requests
from dotenv import load_dotenv

load_dotenv('.env')

API_KEY = '2a51789b2ecc856a96de69ef1b17d42c'


def get_coords(city, str) -> tuple:
    '''Получение координат по названию города'''
    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid{API_KEY}')

    lat = response.json()[0]['lat']
    lon = response.json()[0]['lon']

    return lat, lon


def get_weather(lat: float, lon: float) -> str:
   '''Получение погоды по координатам'''
   response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}')

   print(response.json())



if __name__ == '__main__':
    lat, lon = get_coords('Moscow')
    get_weather(lat, lon)

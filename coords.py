import os
import requests
from unittest.mock import patch
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


@patch('requests.get')
def test_get_weather(mock_get):
    mock_get.return_value.json.return_value = {'main': {'temp': 1}}
    result = get_weather(1, 1)
    assert result == {'main': {'temp': 1}}
    mock_get.assert_called_once_with(
        f'http://api.openweathermap.org/data/2.5/weather'
        f'?lat=1&lon=1&appid={API_KEY}&units=metric&lang=ru'
    )




if __name__ == '__main__':
    lat, lon = get_coords('Moscow')
    weather = get_weather(lat, lon)
    print(weather)
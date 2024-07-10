from .base import WeatherAPIBase
import requests


class OpenMeteo(WeatherAPIBase):
    def __init__(self, lat, long, **kwargs):
        super().__init__(lat, long)

    def get_weather_temp(self):
        params = {'latitude': self.lat, 'longitude': self.long, "current": "temperature_2m"}
        result = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
        result_json = result.json()
        return result_json["current"]["temperature_2m"]


class OpenWeather(WeatherAPIBase):
    def __init__(self, lat, long, **kwargs):
        super().__init__(lat, long)
        self.api_token = kwargs['api_token']

    def get_weather_temp(self):
        params = {'lat': self.lat, 'lon': self.long, "appid": self.api_token}
        result = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        result_json = result.json()
        k = float(result_json["main"]["temp"])
        return k - 273.15

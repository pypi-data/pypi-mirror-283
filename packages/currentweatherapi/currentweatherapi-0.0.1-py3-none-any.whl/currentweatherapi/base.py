from abc import ABC, abstractmethod


class WeatherAPIBase(ABC):
    def __init__(self, lat, long, **kwargs):
        self.lat = lat
        self.long = long

    @abstractmethod
    def get_weather_temp(self):
        pass

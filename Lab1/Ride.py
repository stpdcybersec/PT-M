from datetime import datetime

class Ride:
    def __init__(self, date, fuel_consumption):
        self.__date = date
        self.__fuel_consumption = fuel_consumption

    @property
    def date(self):
        return self.__date

    @property
    def fuel_consumption(self):
        return self.__fuel_consumption

    def __str__(self):
        raise NotImplementedError()

    @staticmethod
    def validate_fuel_consumption(value):
        """Проверка, что расход топлива - положительное число"""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Fuel consumption must be a positive number")
        return value
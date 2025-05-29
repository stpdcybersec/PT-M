from datetime import datetime

class CarPassBase:
    """Базовый класс для записей о проезде автомобилей"""
    
    def __init__(self, pass_date: datetime, car_number: str, fuel_consumption: float):
        """
        Инициализация записи о проезде
        
        Args:
            pass_date (datetime): Дата проезда автомобиля
            car_number (str): Номер автомобиля
            fuel_consumption (float): Расход топлива в литрах на 100 км
        """
        self.__pass_date = pass_date
        self.__car_number = car_number
        self.__fuel_consumption = fuel_consumption
    
    @property
    def pass_date(self) -> datetime:
        """Получить дату проезда"""
        return self.__pass_date

    @property
    def car_number(self) -> str:
        """Получить номер автомобиля"""
        return self.__car_number

    @property
    def fuel_consumption(self) -> float:
        """Получить расход топлива"""
        return self.__fuel_consumption

    def __str__(self) -> str:
        """Строковое представление записи о проезде (должно быть реализовано в подклассах)"""
        raise NotImplementedError()
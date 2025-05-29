from CarPassBase import CarPassBase
from datetime import datetime

class CarPass(CarPassBase):
    """Класс для записи о проезде автомобиля с атрибутом расхода топлива"""
    
    def __init__(self, pass_date: datetime, car_number: str, fuel_consumption: float):
        """
        Инициализация записи о проезде
        
        Args:
            pass_date (datetime): Дата проезда автомобиля
            car_number (str): Номер автомобиля
            fuel_consumption (float): Расход топлива в литрах на 100 км
        """
        super().__init__(pass_date, car_number, fuel_consumption)
    
    def __str__(self) -> str:
        """Строковое представление записи о проезде"""
        return f"{self.pass_date.date().strftime('%Y-%m-%d')},{self.car_number},{self.fuel_consumption}"
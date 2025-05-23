from Ride import Ride

class Motorcycle(Ride):
    def __init__(self, date, license_plate, fuel_consumption):
        super().__init__(date, fuel_consumption)  # Передаем оба параметра в родительский класс
        self.__license_plate = license_plate

    @property
    def license_plate(self):
        return self.__license_plate

    def __str__(self):
        return (f"Type: Motorcycle, Date: {self.date.strftime('%d.%m.%Y')}, "
                f"Plate: {self.license_plate}, "
                f"Fuel: {self.fuel_consumption} L/100km")
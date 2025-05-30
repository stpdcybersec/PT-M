from models.Ride import Ride

class Car(Ride):
    def __init__(self, date, license_plate, fuel_consumption, has_spare_wheel=True):
        super().__init__(date, fuel_consumption)
        self.__license_plate = license_plate
        self.__has_spare_wheel = has_spare_wheel

    @property
    def license_plate(self):
        return self.__license_plate

    @property
    def has_spare_wheel(self):
        return self.__has_spare_wheel

    def __str__(self):
        return f'Type: Car, Date: {self.date.date()}, Plate: {self.license_plate}, Fuel: {self.fuel_consumption}L, Spare wheel: {"Yes" if self.has_spare_wheel else "No"}'
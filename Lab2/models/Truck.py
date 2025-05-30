from models.Ride import Ride

class Truck(Ride):
    def __init__(self, date, plate, fuel_consumption, has_spare_wheel=True):
        super().__init__(date, fuel_consumption)
        self.__plate = plate
        self.__has_spare_wheel = has_spare_wheel

    @property
    def license_plate(self):
        return self.__plate

    @property
    def has_spare_wheel(self):
        return self.__has_spare_wheel

    def __str__(self):
        return f"Type: Truck, Date: {self.date.date()}, Plate: {self.license_plate}, Fuel: {self.fuel_consumption}L, Spare wheel: {'Yes' if self.has_spare_wheel else 'No'}"
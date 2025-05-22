from Ride import Ride

class Car(Ride):
    def __init__(self, date, license_plate):
        super().__init__(date)
        self.__license_plate = license_plate

    @property
    def license_plate(self):
        return self.__license_plate

    def __str__(self):
        return f'Type: Car, Date: {self.date.date()}, Plate: {self.license_plate}'

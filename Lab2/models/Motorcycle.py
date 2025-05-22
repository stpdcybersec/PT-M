from models.Ride import Ride

class Motorcycle(Ride):
    def __init__(self, date, plate):
        super().__init__(date)
        self.__plate = plate

    @property
    def license_plate(self):
        return self.__plate

    def __str__(self):
        return f"Type: Motorcycle, Date: {self.date.date()}, Plate: {self.license_plate}"

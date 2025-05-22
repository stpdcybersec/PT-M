from Ride import Ride

class Truck(Ride):
    def __init__(self, date, plate):
        super().__init__(date)
        self.__plate = plate

    def __str__(self):
        return f"Type: Truck, Date: {self.date.date()}, Plate: {self.__plate}"

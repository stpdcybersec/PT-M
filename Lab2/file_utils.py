import datetime
from models.Car import Car
from models.Truck import Truck
from models.Motorcycle import Motorcycle

def load_rides_from_file(filename):
    rides = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split("(")
            ride_type = parts[0]
            values = parts[1].rstrip(")").split(", ")
            date = datetime.datetime.strptime(values[0], "%d.%m.%Y")
            plate = values[1][1:-1]
            fuel = float(values[2])
            has_spare = True if len(values) < 4 else values[3] == "True"

            if ride_type == "Car":
                rides.append(Car(date, plate, fuel, has_spare))
            elif ride_type == "Truck":
                rides.append(Truck(date, plate, fuel, has_spare))
            elif ride_type == "Motorcycle":
                rides.append(Motorcycle(date, plate, fuel, has_spare))
    return rides

def save_rides_to_file(rides, filename):
    with open(filename, "w") as file:
        for ride in rides:
            file.write(f"{ride.__class__.__name__}({ride.date.strftime('%d.%m.%Y')}, \"{ride.license_plate}\", {ride.fuel_consumption}, {ride.has_spare_wheel})\n")
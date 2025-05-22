import datetime
from models.Car import Car
from models.Truck import Truck
from models.Motorcycle import Motorcycle

def load_rides_from_file(filename):
    rides = []
    with open(filename, "r") as file:
        for line in file:
            ride_type, values = line.strip().split("(")
            values = values.rstrip(")").split(", ")
            date = datetime.datetime.strptime(values[0], "%d.%m.%Y")
            plate = values[1][1:-1]

            if ride_type == "Car":
                rides.append(Car(date, plate))
            elif ride_type == "Truck":
                rides.append(Truck(date, plate))
            elif ride_type == "Motorcycle":
                rides.append(Motorcycle(date, plate))
    return rides

def save_rides_to_file(rides, filename):
    with open(filename, "w") as file:
        for ride in rides:
            file.write(f"{ride.__class__.__name__}({ride.date.strftime('%d.%m.%Y')}, \"{ride.license_plate}\")\n")

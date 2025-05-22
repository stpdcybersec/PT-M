from Car import Car
from Truck import Truck
from Motorcycle import Motorcycle
import datetime

def file_to_rides_list(filename):
    rides = []

    with open(filename, "r") as file:
        for line in file:
            ride_type, values = line.strip().split("(")
            values = values[0:-1].split(", ")

            date = datetime.datetime.strptime(values[0], "%d.%m.%Y")
            plate = values[1][1:-1]  

            if ride_type == "Car":
                rides.append(Car(date, plate))
            elif ride_type == "Truck":
                rides.append(Truck(date, plate))
            elif ride_type == "Motorcycle":
                rides.append(Motorcycle(date, plate))
            else:
                print(f"Unknown transport type: {ride_type}")

    return rides

if __name__ == "__main__":
    rides = file_to_rides_list("supply")
    for ride in rides:
        print(ride)

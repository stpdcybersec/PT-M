from Car import Car
import datetime

def file_to_rides_list(filename):
    rides = []

    with open(filename, "r") as file:
        for line in file:
            ride_type, values = line.strip().split("(")
            values = values[0:-1].split(", ")

            if ride_type == "Car":
                rides.append(
                    Car(
                        date=datetime.datetime.strptime(values[0], "%d.%m.%Y"),
                        license_plate=values[1][1:-1]  # убираем кавычки
                    )
                )
    return rides

if __name__ == "__main__":
    rides = file_to_rides_list('supply')
    for ride in rides:
        print(ride)

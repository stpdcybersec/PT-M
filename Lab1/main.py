from Car import Car
from Truck import Truck
from Motorcycle import Motorcycle
import datetime

def file_to_rides_list(filename):
    rides = []
    
    with open(filename, "r", encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            try:
                line = line.strip()
                if not line:
                    continue
                
                # Разделяем строку на тип и параметры
                ride_type, values_part = line.split("(", 1)
                values_part = values_part.rstrip(")")
                values = [v.strip() for v in values_part.split(",")]
                
                # Проверяем количество параметров
                if len(values) != 3:
                    raise ValueError(f"Expected 3 parameters, got {len(values)}")
                
                # Обрабатываем дату
                date = datetime.datetime.strptime(values[0], "%d.%m.%Y")
                
                # Обрабатываем номер (удаляем кавычки)
                plate = values[1].strip('"\'')
                
                # Обрабатываем расход топлива
                try:
                    fuel = float(values[2])
                except ValueError:
                    raise ValueError("Fuel consumption must be a number")
                
                # Создаем объект
                if ride_type == "Car":
                    rides.append(Car(date, plate, fuel))
                elif ride_type == "Truck":
                    rides.append(Truck(date, plate, fuel))
                elif ride_type == "Motorcycle":
                    rides.append(Motorcycle(date, plate, fuel))
                else:
                    print(f"Unknown transport type: {ride_type} in line {line_num}")
                    
            except ValueError as e:
                print(f"Error in line {line_num}: {e}. Line: '{line}'")
            except Exception as e:
                print(f"Unexpected error in line {line_num}: {e.__class__.__name__}: {e}. Line: '{line}'")
    
    return rides

if __name__ == "__main__":
    try:
        rides = file_to_rides_list("supply")
        for ride in rides:
            print(ride)
    except FileNotFoundError:
        print("Error: File 'supply' not found")
    except Exception as e:
        print(f"Unexpected error: {e.__class__.__name__}: {e}")
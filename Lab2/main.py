import tkinter as tk
from tkinter import ttk, messagebox
from file_utils import load_rides_from_file, save_rides_to_file
from models.Car import Car
from models.Truck import Truck
from models.Motorcycle import Motorcycle
from models.Ride import Ride
import datetime

FILENAME = "supply"

class RideApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fixation of Vehicle Passes")

        self.rides = load_rides_from_file(FILENAME)
        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        # Table
        columns = ("Type", "Date", "Plate", "Fuel Consumption", "Spare Wheel")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Entry section
        form = tk.Frame(self.root)
        form.pack(pady=10)

        self.type_var = tk.StringVar(value="Car")
        self.date_var = tk.StringVar()
        self.plate_var = tk.StringVar()
        self.fuel_var = tk.StringVar()
        self.spare_var = tk.BooleanVar(value=True)

        tk.Label(form, text="Type").grid(row=0, column=0)
        tk.OptionMenu(form, self.type_var, "Car", "Truck", "Motorcycle").grid(row=0, column=1)

        tk.Label(form, text="Date (dd.mm.yyyy)").grid(row=0, column=2)
        tk.Entry(form, textvariable=self.date_var).grid(row=0, column=3)

        tk.Label(form, text="Plate").grid(row=0, column=4)
        tk.Entry(form, textvariable=self.plate_var).grid(row=0, column=5)

        tk.Label(form, text="Fuel (L)").grid(row=0, column=6)
        tk.Entry(form, textvariable=self.fuel_var).grid(row=0, column=7)

        tk.Checkbutton(form, text="Has Spare Wheel", variable=self.spare_var).grid(row=0, column=8)

        tk.Button(form, text="Add", command=self.add_ride).grid(row=0, column=9)
        tk.Button(form, text="Delete Selected", command=self.delete_selected).grid(row=0, column=10)

    def populate_table(self):
        for ride in self.rides:
            self.tree.insert("", tk.END, values=(
                ride.__class__.__name__, 
                ride.date.date(), 
                ride.license_plate,
                ride.fuel_consumption,
                "Yes" if ride.has_spare_wheel else "No"
            ))

    def add_ride(self):
        try:
            date = datetime.datetime.strptime(self.date_var.get(), "%d.%m.%Y")
            plate = self.plate_var.get()
            fuel = float(self.fuel_var.get())
            rtype = self.type_var.get()
            has_spare = self.spare_var.get()

            if rtype == "Car":
                ride = Car(date, plate, fuel, has_spare)
            elif rtype == "Truck":
                ride = Truck(date, plate, fuel, has_spare)
            elif rtype == "Motorcycle":
                ride = Motorcycle(date, plate, fuel, has_spare)
            else:
                raise ValueError("Invalid type")

            self.rides.append(ride)
            self.tree.insert("", tk.END, values=(
                rtype, 
                date.date(), 
                plate, 
                fuel,
                "Yes" if has_spare else "No"
            ))
            save_rides_to_file(self.rides, FILENAME)

            self.date_var.set("")
            self.plate_var.set("")
            self.fuel_var.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        for item in selected:
            values = self.tree.item(item)["values"]
            for ride in self.rides:
                if (ride.__class__.__name__ == values[0] and 
                    str(ride.date.date()) == values[1] and 
                    ride.license_plate == values[2] and
                    ride.fuel_consumption == float(values[3])):
                    self.rides.remove(ride)
                    break
            self.tree.delete(item)
        save_rides_to_file(self.rides, FILENAME)

if __name__ == "__main__":
    root = tk.Tk()
    app = RideApp(root)
    root.mainloop()
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Make: {self.make}\nModel: {self.model}\nYear: {self.year}\n")

    def calculate_mileage(self):
        return None

    def towing_capacity(self):
        return None

class Car(Vehicle):
    def __init__(self, make, model, year, lt_per_100km):
        super().__init__(make, model, year)
        self.lt_per_100km = lt_per_100km

    def calculate_mileage(self, distance):
        return distance / 100 * self.lt_per_100km

    def calculate_price(self, distance, price_per_litre):
        return distance / 100 * self.lt_per_100km * price_per_litre


class Motorcycle(Vehicle):
    def __init__(self, make, model, year, lt_per_100km):
        super().__init__(make, model, year)
        self.lt_per_100km = lt_per_100km

    def calculate_mileage(self, distance):
        return distance / 100 * self.lt_per_100km

    def calculate_price(self, distance, price_per_litre):
        return distance / 100 * self.lt_per_100km * price_per_litre


class Truck(Vehicle):
    def __init__(self, make, model, year, lt_per_100km, towing_capacity):
        super().__init__(make, model, year)
        self.lt_per_100km = lt_per_100km
        self.towing_capacity_value = towing_capacity

    def calculate_mileage(self, distance):
        return (distance / 100) * self.lt_per_100km

    def towing_capacity(self):
        print(f"Towing Capacity: {self.towing_capacity_value} kg")
        return self.towing_capacity_value


def main():
    my_car = Car(make="BMW", model="Seria 1", year=2007, lt_per_100km=6.9)
    my_car.display_info()
    consum = my_car.calculate_mileage(distance=365)
    cheltuieli = my_car.calculate_price(distance=365, price_per_litre=7.08)
    print(f"Consum pentru 365 km: {consum} litri")
    print(f"Cost pentru 365 km: {cheltuieli} lei")


    my_motorcycle = Motorcycle(make="Yamaha", model="YZF-R3", year=2021, lt_per_100km=3.7)
    my_motorcycle.display_info()
    moto_consum = my_motorcycle.calculate_mileage(distance=365)
    moto_cost = my_motorcycle.calculate_price(distance=365, price_per_litre=7.08)
    print(f"Consum Motorcycle pentru 365 km: {moto_consum} litri")
    print(f"Cost Motorcycle pentru 365 km: {moto_cost} lei\n")

    my_truck = Truck(make="Volvo", model="FH16", year=2009, lt_per_100km=13.6, towing_capacity= 650)
    my_truck.display_info()
    my_truck.towing_capacity()


if __name__ == "__main__":
    main()
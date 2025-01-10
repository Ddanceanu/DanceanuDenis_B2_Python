class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Nume: {self.name}")
        print(f"Vârstă: {self.age} ani\n")


class Mammal(Animal):
    def __init__(self, name, age, has_fur):
        super().__init__(name, age)
        self.has_fur = has_fur

    def protective(self):
        print("Mamiferele sunt foarte protectoare cu copiii lor.\n")

    def display_fur(self):
        if self.has_fur:
            print(f"Mamiferul {self.name.lower()} are blană.")
        else:
            print(f"Mamiferul {self.name.lower()} nu are blană.")
        print()


class Bird(Animal):
    def __init__(self, name, age, can_fly):
        super().__init__(name, age)
        self.can_fly = can_fly

    def lay_eggs(self):
        print(f"Pasarea {self.name.lower()} depune oua.")

    def display_flying_ability(self):
        if self.can_fly:
            print(f"Pasarea {self.name.lower()} poate zbura.")
        else:
            print(f"Pasarea {self.name.lower()} nu poate zbura.")
        print()


class Fish(Animal):
    def __init__(self, name, age, has_gills):
        super().__init__(name, age)
        self.has_gills = has_gills

    def swim(self):
        print(f"Pestele {self.name.lower()} inoata.")

    def display_gills(self):
        if self.has_gills:
            print(f"Pestele {self.name.lower()} are branhii.")
        else:
            print(f"Pestele {self.name.lower()} nu are branhii.")
        print()


def main():
    mamifer = Mammal(name="Caine", age=3, has_fur=True)
    mamifer.display_info()
    mamifer.protective()
    mamifer.display_fur()

    pasare = Bird(name="Barza", age=2, can_fly=True)
    pasare.display_info()
    pasare.lay_eggs()
    pasare.display_flying_ability()

    peste = Fish(name="Crap", age=1, has_gills=True)
    peste.display_info()
    peste.swim()
    peste.display_gills()

if __name__ == "__main__":
    main()

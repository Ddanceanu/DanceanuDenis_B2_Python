class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display_name(self):
        print(f"Nume: {self.name}")
        print(f"Salariu: {self.salary}\n")

class Manager(Employee):
    def __init__(self, name, salary):
        super().__init__(name, salary)
        self.team = []

    def add_in_team(self, employee):
        if isinstance(employee, Employee):
            self.team.append(employee)
        else:
            print(f"Error: {employee} is not an Employee")

    def show_team(self):
        print(f"Echipa lui {self.name}:")
        for member in self.team:
            print(f"- {member.name}")


class Engineer(Employee):
    def __init__(self, name, salary):
        super().__init__(name, salary)

    def display_task(self):
        print(f"{self.name} se ocupe de rezolvarea problemelor ce pot aparea.\n")

class Salesperson(Employee):
    def __init__(self, name, salary):
        super().__init__(name, salary)

    def display_task(self):
        print(f"{self.name} cauta noi clienti pentru promovarea produsului..\n")


def main():
    first = Employee("Andrei", 2700)
    second = Employee("Marius", 3200)
    third = Manager("Denis", 8900)
    third.add_in_team(first)
    third.add_in_team(second)
    third.show_team()
    engineer = Engineer("Ioana", 4500)
    engineer.display_name()
    engineer.display_task()
    salesperson = Salesperson("Alex", 4000)
    salesperson.display_name()
    salesperson.display_task()

    
if __name__ == "__main__":
    main()
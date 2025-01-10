class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print("Deposit successful!")
        print(f"New account balance: {self.balance}\n")

    def withdraw(self, amount):
        if (amount > self.balance):
            print("Insufficient funds")
            print("Disponible balance: ", self.balance)
        else:
            self.balance -= amount
            print("Withdraw successful!")
            print(f"New account balance: {self.balance}\n")

    def calc_interest(self, interest):
        return None


class SavingsAccount(Account):
    def __init__(self, name, balance, interest):
        super().__init__(name, balance)
        self.interest = interest

    def calc_interest(self):
        interest = self.balance * self.interest
        self.balance += interest
        print(f"Interest added: {interest}")
        print(f"New balance after interest: {self.balance}")
        return interest


class CheckingAccount(Account):
    def __init__(self, name, balance, interest):
        super().__init__(name, balance)
        self.interest = interest

    def calc_interest(self):
        print(f"Account balance: {self.balance}")
        print("If you will add $500 every year, in 5 years you will have:\n")
        i = 1
        while i <= 5:
            new_balance = self.interest * self.balance + self.balance
            print(f"Year: {i}, bank account after interest: {new_balance}")
            self.balance += 500
            i = i + 1


def main():
    savings = SavingsAccount(name="Denis", balance=1000, interest=0.05)
    savings.deposit(500)
    savings.withdraw(200)
    savings.calc_interest()

    print("\n")

    test = CheckingAccount(name="Andrei", balance=1500, interest=0.02)
    test.calc_interest()

if __name__ == '__main__':
    main()

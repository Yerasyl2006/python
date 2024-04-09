class Account():
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, money):
        self.balance += money

    def withdraw(self, money):
        self.balance -= money
        if(self.balance < 0):
            print("You have not enough money")
        else:
            print(self.balance)

wallet = Account("Dulat", 50000)
wallet.deposit(5000)
wallet.withdraw(10000)
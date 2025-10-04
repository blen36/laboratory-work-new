class Bank:
    def __init__(self):
        self.clients = {} #словарик айди клиента - имя клиента
    def register_client(self, name):
        pass
    def open_account(self):
        pass

class Client:
    def __init__(self, client_id, name):
        self.client_id = client_id
        self.name = name
        self.accounts = {}  #словарик валюта - банковский счет

    def add_account(self, currency):
        if currency in self.accounts:
            raise DuplicateAccount(f"Счет в валюте {currency} уже существует.")
        self.accounts[currency] = BankAccount(self.client_id, currency)

    def remove_account(self, currency):
        if currency not in self.accounts:
            raise AccountNotFound(f"Нет счета в валюте {currency}.")
        del self.accounts[currency]

    def get_account(self, currency):
        if currency not in self.accounts:
            raise AccountNotFound(f"Нет счета в валюте {currency}.")
        return self.accounts[currency]

    def get_total_balance(self):
        return sum(acc.balance for acc in self.accounts.values())

    def __str__(self):
        return f"{self.name} (ID: {self.client_id})"

class BankAccount:
    def __init__(self, owner_id, currency, balance = 0):
        self.owner_id = owner_id
        self.currency = currency
        self.balance = float(balance)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError('Сумма должна быть положительной.')
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError('Сумма должна быть положительной.')
        if amount > self.balance:
            raise InsufficientFunds("Недостаточно средст на счете.")
        self.balance -= amount

    def __str__(self):
        return f"{self.currency}: {self.balance:.2f}"
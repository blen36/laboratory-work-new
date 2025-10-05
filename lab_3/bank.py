class BankError(Exception):
    pass

class AccountNotFound(BankError):
    pass

class DuplicateAccount(BankError):
    pass

class InsufficientFunds(BankError):
    pass

class ClientNotFound(BankError):
    pass

class Bank:
    def __init__(self):
        self.clients = {} #словарик айди клиента - имя клиента

    def register_client(self, client_id, name):
        if client_id in self.clients:
            raise ValueError(f"Клиент с ID: {client_id} уже существует")
        client = Client(client_id, name)
        self.clients[client_id] = client
        print(f"Клиент {name} зарегистрирован. ID: {client_id}")

    def get_client(self, client_id):
        if client_id not in self.clients:
            raise ClientNotFound(f"Клиент с ID: {client_id} не найден.")
        return self.clients[client_id] #возвращает объект класса Client

    def open_account(self, client_id, currency):
        client = self.get_client(client_id)
        client.add_account(currency)

    def close_account(self, client_id, currency):
        client = self.get_client(client_id)
        client.remove_account(currency)
        print(f"Счет {currency} закрыт для клиента {client.name}.")

    def deposit(self, client_id, currency, amount):
        client = self.get_client(client_id)
        acc = client.get_account(currency)
        acc.deposit(amount)
        print(f"На счет {currency} зачислено {amount:.2f}. ")

    def withdraw(self, client_id, currency, amount):
        client = self.get_client(client_id)
        acc = client.get_account(currency)
        acc.withdraw(amount)
        print(f"Со счета {currency} снято {amount:.2f}. ")

    def transfer(self, client_id, from_currency, to_currency, amount):
        client = self.get_client(client_id)
        acc_from = client.get_account(from_currency)
        acc_to = client.get_account(to_currency)
        acc_from.withdraw(amount)
        acc_to.deposit(amount)
        print(f"Переведено {amount:.2f} из счета {from_currency} на счет {to_currency}.")

    def print_statements(self, client_id):
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

def main():
    bank = Bank()

    while True:
        print("\n=== БАНКОВСКАЯ СИСТЕМА ===")
        print("1. Зарегистрировать клиента")
        print("2. Открыть счет")
        print("3. Закрыть счет")
        print("4. Пополнить счет")
        print("5. Снять деньги")
        print("6. Перевести между своими счетами")
        print("7. Выписка по счетам")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                client_id = input("Введите ID клиента (например, 001): ")
                name = input("Введите имя клиента: ")
                bank.register_client(client_id, name)

            elif choice == "2":
                client_id = input("Введите ID клиента: ")
                currency = input("Введите валюту (BYN/USD/EUR): ").upper()
                bank.open_account(client_id, currency)

            elif choice == "3":
                client_id = input("Введите ID клиента: ")
                currency = input("Введите валюту для закрытия: ").upper()
                bank.close_account(client_id, currency)

            elif choice == "4":
                client_id = input("Введите ID клиента: ")
                currency = input("Введите валюту: ").upper()
                amount = float(input("Введите сумму: "))
                bank.deposit(client_id, currency, amount)

            elif choice == "5":
                client_id = input("Введите ID клиента: ")
                currency = input("Введите валюту: ").upper()
                amount = float(input("Введите сумму: "))
                bank.withdraw(client_id, currency, amount)

            elif choice == "6":
                client_id = input("Введите ID клиента: ")
                from_currency = input("С какой валюты перевести: ").upper()
                to_currency = input("На какую валюту перевести: ").upper()
                amount = float(input("Введите сумму: "))
                bank.transfer(client_id, from_currency, to_currency, amount)

            elif choice == "7":
                client_id = input("Введите ID клиента: ")
                bank.print_statement(client_id)
        finally:
            print("...")
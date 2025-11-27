class AccountNotFound(Exception):
    pass

class DuplicateAccount(Exception):
    pass

class InsufficientFunds(Exception):
    pass

class ClientNotFound(Exception):
    pass

CURRENCY_RATES = {"BYN": 1.0, "USD": 3.0, "EUR": 3.98}

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
        currency = currency.upper()
        if currency not in CURRENCY_RATES:
            raise ValueError(f"Некорректная валюта: {currency}. Доступные: {', '.join(CURRENCY_RATES.keys())}")
        client = self.get_client(client_id)
        client.add_account(currency)
        print(f"Счет {currency} открыт для клиента {client.name}.")

    def close_account(self, client_id, currency):
        client = self.get_client(client_id)
        client.remove_account(currency)
        print(f"Счет {currency} закрыт для клиента {client.name}.")

    def deposit(self, client_id, currency, amount, deposit_currency = None):
        if deposit_currency is None:
            deposit_currency = currency

        deposit_currency = deposit_currency.upper()
        currency = currency.upper()

        client = self.get_client(client_id)
        acc = client.get_account(currency)

        if deposit_currency != currency:
            amount_in_byn = amount * CURRENCY_RATES[deposit_currency]
            amount_converted = amount_in_byn / CURRENCY_RATES[currency]
            acc.deposit(amount_converted)
            print(
                f"На счет {currency} зачислено {amount_converted:.2f} (конвертировано из {amount:.2f} {deposit_currency}).")
        else:
            acc.deposit(amount)
            print(f"На счет {currency} зачислено {amount:.2f}.")

    def withdraw(self, client_id, currency, amount, withdraw_currency = None):
        if withdraw_currency is None:
            withdraw_currency = currency

        withdraw_currency = withdraw_currency.upper()
        currency = currency.upper()

        client = self.get_client(client_id)
        acc = client.get_account(currency)

        if withdraw_currency != currency:
            amount_in_byn = amount * CURRENCY_RATES[withdraw_currency]
            amount_converted = amount_in_byn / CURRENCY_RATES[currency]
            if amount_converted > acc.balance:
                raise InsufficientFunds(f"Недостаточно средств на счете {currency}. "
                                        f"Требуется: {amount_converted:.2f} {currency}, "
                                        f"доступно: {acc.balance:.2f} {currency}.")
            acc.withdraw(amount_converted)
            print(f"Со счета {currency} снято {amount:.2f} {withdraw_currency} "
                  f"(конвертировано в {amount_converted:.2f} {currency}).")
        else:
            acc.withdraw(amount)
            print(f"Со счета {currency} снято {amount:.2f}.")

    def transfer(self, from_client_id, from_currency, to_client_id, to_currency, amount):
        sender = self.get_client(from_client_id)
        receiver = self.get_client(to_client_id)

        acc_from = sender.get_account(from_currency)
        acc_to = receiver.get_account(to_currency)

        acc_from.withdraw(amount)

        amount_in_byn = amount * CURRENCY_RATES[from_currency]
        amount_converted = amount_in_byn / CURRENCY_RATES[to_currency]

        acc_to.deposit(amount_converted)
        f"Переведено {amount:.2f} {from_currency} от {sender.name} "
        f"к {receiver.name} ({amount_converted:.2f} {to_currency} после конверсии)."

    def print_statement(self, client_id):
        client = self.get_client(client_id)
        filename = f"{client.name}.txt"
        with open(filename, "w", encoding = "utf-8") as f:
            f.write(f"Выписка по клиенту: {client.name} (ID: {client.client_id})\n\n ")
            total_byn = 0
            for acc in client.accounts.values():
                f.write(f"{acc.currency}: {acc.balance:.2f}\n")
                total_byn += acc.balance * CURRENCY_RATES[acc.currency]
            f.write(f"\nОбщий баланс (в BYN): {total_byn:.2f}\n")
        print(f"Выписка сохранена в файл {filename}.")

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
            raise InsufficientFunds("Недостаточно средств на счете.")
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
        print("6. Перевести между счетами")
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
                currency = input("Введите валюту счета: ").upper()
                amount = float(input("Введите сумму: "))
                deposit_currency = input(
                    "Введите валюту пополнения (или Enter для использования валюты счета): ").upper()
                if not deposit_currency:
                    bank.deposit(client_id, currency, amount)
                else:
                    bank.deposit(client_id, currency, amount, deposit_currency)


            elif choice == "5":
                client_id = input("Введите ID клиента: ")
                currency = input("Введите валюту счета: ").upper()
                amount = float(input("Введите сумму: "))
                withdraw_currency = input("Введите валюту снятия (или Enter для использования валюты счета): ").upper()
                if not withdraw_currency:
                    bank.withdraw(client_id, currency, amount)
                else:
                    bank.withdraw(client_id, currency, amount, withdraw_currency)

            elif choice == "6":
                from_client_id = input("Введите ID отправителя: ")
                from_currency = input("С какой валюты перевести: ").upper()
                to_client_id = input("Введите ID получателя: ")
                to_currency = input("На какую валюту зачислить: ").upper()
                amount = float(input("Введите сумму: "))
                bank.transfer(from_client_id, from_currency, to_client_id, to_currency, amount)

            elif choice == "7":
                client_id = input("Введите ID клиента: ")
                bank.print_statement(client_id)

            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

        except Exception as e:
            print("Ошибка: ", e)

if __name__ == "__main__":
    main()
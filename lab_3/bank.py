class Client:
    def __init__(self, client_id: int, name: str, phone: str):
        self.client_id = client_id
        self.name = name
        self.phone = phone
        self.accounts = {}  # словарь: валюта -> счет

    def __str__(self):
        return f"Клиент {self.client_id}: {self.name}"
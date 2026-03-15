class Customer:
    """Stores customer information and their order history."""

    def __init__(self, customer_id: str, name: str, email: str):
        self._customer_id = customer_id
        self._name = name
        self._email = email
        self._orders: list = []

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    def add_order(self, order):
        self._orders.append(order)

    def get_orders(self) -> list:
        return list(self._orders)

    def __str__(self) -> str:
        return f"Customer: {self._name} | Email: {self._email}"

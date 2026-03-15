from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class for all products in the store."""

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    # --- Getters (Encapsulation) ---

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def stock(self) -> int:
        return self._stock

    def reduce_stock(self, quantity: int):
        """Decrease available stock after a purchase."""
        if quantity > self._stock:
            raise ValueError(f"Not enough stock for '{self._name}'. Available: {self._stock}.")
        self._stock -= quantity

    # --- Abstract methods (Abstraction + Polymorphism) ---

    @abstractmethod
    def get_info(self) -> str:
        """Return a human-readable description of the product."""
        pass

    @abstractmethod
    def calculate_shipping(self) -> float:
        """Return the shipping cost for one unit of this product."""
        pass

    def __str__(self) -> str:
        return f"{self._name} (${self._price:.2f})"


class PhysicalProduct(Product):
    """A tangible product that requires shipping."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight_kg: float):
        super().__init__(product_id, name, price, stock)
        self._weight_kg = weight_kg

    @property
    def weight_kg(self) -> float:
        return self._weight_kg

    def get_info(self) -> str:
        return (
            f"[Physical] {self._name} | "
            f"Price: ${self._price:.2f} | "
            f"Weight: {self._weight_kg} kg | "
            f"Stock: {self._stock}"
        )

    def calculate_shipping(self) -> float:
        """Shipping cost = $2.50 per kilogram."""
        return round(self._weight_kg * 2.50, 2)


class DigitalProduct(Product):
    """A downloadable product with no physical shipping."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, download_url: str):
        super().__init__(product_id, name, price, stock)
        self._download_url = download_url

    @property
    def download_url(self) -> str:
        return self._download_url

    def get_info(self) -> str:
        return (
            f"[Digital]  {self._name} | "
            f"Price: ${self._price:.2f} | "
            f"Download: {self._download_url}"
        )

    def calculate_shipping(self) -> float:
        """Digital products are delivered online — no shipping cost."""
        return 0.0

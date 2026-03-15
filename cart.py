class CartItem:
    """Represents one product line in the shopping cart."""

    def __init__(self, product, quantity: int):
        self._product = product
        self._quantity = quantity

    @property
    def product(self):
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 1:
            raise ValueError("Quantity must be at least 1.")
        self._quantity = value

    def get_subtotal(self) -> float:
        return round(self._product.price * self._quantity, 2)

    def __str__(self) -> str:
        return f"{self._product.name} x{self._quantity} = ${self.get_subtotal():.2f}"


class Cart:
    """Shopping cart that holds CartItems and calculates totals."""

    def __init__(self):
        self._items: dict = {}  # product_id -> CartItem

    # --- Item management ---

    def add_product(self, product, quantity: int = 1):
        """Add a product to the cart. Raises ValueError if stock is insufficient."""
        if product.stock < quantity:
            raise ValueError(f"Not enough stock for '{product.name}'. Available: {product.stock}.")
        if product.product_id in self._items:
            self._items[product.product_id].quantity += quantity
        else:
            self._items[product.product_id] = CartItem(product, quantity)

    def remove_product(self, product_id: str):
        """Remove a product line from the cart entirely."""
        if product_id not in self._items:
            raise ValueError("Product is not in the cart.")
        del self._items[product_id]

    def clear(self):
        """Empty the cart."""
        self._items.clear()

    # --- Totals ---

    def get_total(self) -> float:
        """Sum of all item subtotals (without shipping)."""
        return round(sum(item.get_subtotal() for item in self._items.values()), 2)

    def get_shipping_total(self) -> float:
        """Sum of shipping costs for all items."""
        return round(
            sum(item.product.calculate_shipping() * item.quantity for item in self._items.values()),
            2,
        )

    def get_grand_total(self) -> float:
        return round(self.get_total() + self.get_shipping_total(), 2)

    # --- Helpers ---

    def is_empty(self) -> bool:
        return len(self._items) == 0

    @property
    def items(self) -> list:
        return list(self._items.values())

    def __str__(self) -> str:
        if self.is_empty():
            return "Cart is empty."
        lines = ["Shopping Cart:"]
        for item in self._items.values():
            lines.append(f"  {item}")
        lines.append(f"  Subtotal : ${self.get_total():.2f}")
        lines.append(f"  Shipping : ${self.get_shipping_total():.2f}")
        lines.append(f"  Grand Total: ${self.get_grand_total():.2f}")
        return "\n".join(lines)

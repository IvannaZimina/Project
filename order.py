from enum import Enum
from datetime import datetime


class OrderStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class Order:
    """Represents a completed purchase. Created by Store.checkout()."""

    _next_id = 1  # class-level counter for auto-incrementing IDs

    def __init__(self, customer, items: list, total: float, shipping_total: float):
        self._order_id = Order._next_id
        Order._next_id += 1

        self._customer = customer
        self._items = items            # snapshot of CartItems at checkout time
        self._total = total
        self._shipping_total = shipping_total
        self._status = OrderStatus.PENDING
        self._created_at = datetime.now()

    # --- Properties ---

    @property
    def order_id(self) -> int:
        return self._order_id

    @property
    def customer(self):
        return self._customer

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def total(self) -> float:
        return self._total

    @property
    def shipping_total(self) -> float:
        return self._shipping_total

    @property
    def grand_total(self) -> float:
        return round(self._total + self._shipping_total, 2)

    @property
    def created_at(self) -> datetime:
        return self._created_at

    # --- Status update ---

    def update_status(self, new_status: OrderStatus):
        self._status = new_status

    def __str__(self) -> str:
        lines = [
            f"Order #{self._order_id}",
            f"  Customer  : {self._customer.name}",
            f"  Status    : {self._status.value}",
            f"  Date      : {self._created_at.strftime('%Y-%m-%d %H:%M')}",
            "  Items:",
        ]
        for item in self._items:
            lines.append(f"    - {item}")
        lines.append(f"  Subtotal  : ${self._total:.2f}")
        lines.append(f"  Shipping  : ${self._shipping_total:.2f}")
        lines.append(f"  Grand Total: ${self.grand_total:.2f}")
        return "\n".join(lines)

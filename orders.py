from order import Order

class OrderManager:
    """Handles order management for the store."""

    def __init__(self):
        self._orders = []

    def add_order(self, order: Order):
        """Add a new order to the order history."""
        self._orders.append(order)

    def get_all_orders(self):
        """Retrieve all orders as a list."""
        return list(self._orders)

    def get_order_by_id(self, order_id):
        """Retrieve a specific order by its ID."""
        for order in self._orders:
            if order.order_id == order_id:
                return order
        raise ValueError(f"Order with ID '{order_id}' not found.")
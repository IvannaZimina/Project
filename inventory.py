class InventoryManager:
    """Handles stock management for the store."""

    def __init__(self):
        self._stock = {}

    def add_product(self, product):
        """Add or update a product in the inventory."""
        self._stock[product.product_id] = product

    def reduce_stock(self, product_id, quantity):
        """Reduce the stock of a product by the given quantity."""
        if product_id not in self._stock:
            raise ValueError(f"Product '{product_id}' not found in inventory.")
        product = self._stock[product_id]
        if product.stock < quantity:
            raise ValueError(f"Not enough stock for product '{product_id}'.")
        product.reduce_stock(quantity)

    def get_product(self, product_id):
        """Retrieve a product by its ID."""
        if product_id not in self._stock:
            raise ValueError(f"Product '{product_id}' not found in inventory.")
        return self._stock[product_id]

    def list_products(self):
        """List all products in the inventory."""
        return list(self._stock.values())
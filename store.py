from order import Order
from checkout_processor import CheckoutProcessor
from inventory import InventoryManager
from orders import OrderManager


class Store:
    """
    This file describes the "Store" class, which manages the product catalog and order processing:
      - Stores a list of available products (catalog).
      - Allows adding products to the catalog.
      - Processes orders: checks the cart, reduces stock, creates an order.
    """

    def __init__(self, name: str):
        """Create a store with a name, inventory, and order manager."""
        self._name = name
        self._inventory = InventoryManager()
        self._orders = OrderManager()
        self._checkout_processor = CheckoutProcessor()

    @property
    def name(self) -> str:
        return self._name

    # --- Catalog management ---

    """Add or replace a product in the store's inventory.
    Used in main.py to set up the initial products before customers start shopping."""
    def add_product(self, product):
        self._inventory.add_product(product)

    """Return one product by id from the inventory, or raise an error if not found.
    Used in main.py when customers add products to their carts."""
    def get_product(self, product_id: str):
        return self._inventory.get_product(product_id)

    """Return all catalog products as a list.
    Used in main.py to show remaining stock after purchases."""
    def list_products(self):
        return self._inventory.list_products()

    """Print the catalog in a readable format.
    Used in main.py to show the products before customers add them to their carts."""
    def display_catalog(self):
        # Prints the top border of the catalog
        print(f"\n{'=' * 55}")
        print(f"  {self._name} — Product Catalog")
        # Prints the bottom border of the title
        print(f"{'=' * 55}")
        # Iterates through all products in the catalog and prints their information
        for product in self._inventory.list_products():
            print(f"  [{product.product_id}] {product.get_info()}")
        # Prints the bottom border of the catalog
        print(f"{'=' * 55}\n")

    # --- Checkout ---

    """Complete checkout: validate cart, reduce stock, create order, clear cart.
        Realized in CheckoutProcessor, but called from main.py via the store."""
    def checkout(self, customer, cart) -> Order:
        order = self._checkout_processor.process_checkout(customer, cart, self._orders)
        self._orders.add_order(order)
        # Returns the created Order object.
        return order

    # --- Order history ---

    """Retrieve all orders from the order manager."""
    def get_all_orders(self):
        return self._orders.get_all_orders()

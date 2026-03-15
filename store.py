from order import Order


class Store:
    """
    Central class that manages the product catalog and processes checkouts.

    Responsibilities (Single Responsibility kept per class):
      - Maintain the catalog of available products.
      - Process the checkout: validate the cart, reduce stock, create an Order.
    """

    def __init__(self, name: str):
        self._name = name
        self._catalog: dict = {}  # product_id -> Product
        self._orders: list = []

    @property
    def name(self) -> str:
        return self._name

    # --- Catalog management ---

    def add_product(self, product):
        self._catalog[product.product_id] = product

    def get_product(self, product_id: str):
        if product_id not in self._catalog:
            raise ValueError(f"Product '{product_id}' not found in catalog.")
        return self._catalog[product_id]

    def list_products(self) -> list:
        return list(self._catalog.values())

    def display_catalog(self):
        print(f"\n{'=' * 55}")
        print(f"  {self._name} — Product Catalog")
        print(f"{'=' * 55}")
        for product in self._catalog.values():
            print(f"  [{product.product_id}] {product.get_info()}")
        print(f"{'=' * 55}\n")

    # --- Checkout ---

    def checkout(self, customer, cart) -> Order:
        """
        Process a purchase:
          1. Validate the cart is not empty.
          2. Reduce stock for each item.
          3. Create and store an Order.
          4. Clear the cart.
        Returns the created Order.
        """
        if cart.is_empty():
            raise ValueError("Cannot checkout with an empty cart.")

        for item in cart.items:
            item.product.reduce_stock(item.quantity)

        order = Order(
            customer=customer,
            items=list(cart.items),
            total=cart.get_total(),
            shipping_total=cart.get_shipping_total(),
        )

        customer.add_order(order)
        self._orders.append(order)
        cart.clear()

        return order

    # --- Order history ---

    def get_all_orders(self) -> list:
        return list(self._orders)

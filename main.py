"""
main.py — Demo script for the Online Storefront project.

Run:  python main.py
"""

from store import Store
from cart import Cart
from customer import Customer
from factory import ProductFactory
from order import OrderStatus
from checkout_processor import CheckoutProcessor


def main():
    # ------------------------------------------------------------------ #
    #  1. Set up the store and populate the catalog via ProductFactory     #
    # ------------------------------------------------------------------ #
    store = Store("Python Online Storefront")

    # Product list, as if it were loaded from a database.
    # The type is explicit: "physical" or "digital".
    products_data = [
        # Physical products: they have weight and require shipping.
        {
            "product_type": "physical",
            "product_id": "P001",
            "name": "Laptop",
            "price": 999.99,
            "stock": 10,
            "weight_kg": 2.5
        },
        {
            "product_type": "physical",
            "product_id": "P002",
            "name": "Wireless Headphones",
            "price": 79.99,
            "stock": 25,
            "weight_kg": 0.3
        },
        {
            "product_type": "physical",
            "product_id": "P003",
            "name": "Mechanical Keyboard",
            "price": 129.99,
            "stock": 15,
            "weight_kg": 1.1
        },
        # Digital products: they are downloadable and do not require shipping.
        {
            "product_type": "digital",
            "product_id": "D001",
            "name": "Python OOP Guide (eBook)",
            "price": 19.99,
            "stock": 100,
            "download_url": "https://store.example.com/dl/oop-guide"
        },
        {
            "product_type": "digital",
            "product_id": "D002",
            "name": "Web Development Course",
            "price": 49.99,
            "stock": 50,
            "download_url": "https://store.example.com/dl/webdev"
        },
    ]

    # Add each product to the store through the factory.
    for product_info in products_data:
        product = ProductFactory.create(**product_info)
        store.add_product(product)

    store.display_catalog()

    # ------------------------------------------------------------------ #
    #  2. Customer browses the store and adds items to their cart          #
    # ------------------------------------------------------------------ #
    customer = Customer("C001", "Alice Smith", "alice@example.com")
    print(customer)

    cart = Cart()
    cart.add_product(store.get_product("P002"), quantity=2)   # 2 × Headphones
    cart.add_product(store.get_product("D001"), quantity=1)   # 1 × eBook
    cart.add_product(store.get_product("D002"), quantity=1)   # 1 × Course

    print("\n" + str(cart))

    # ------------------------------------------------------------------ #
    #  3. Checkout → Order is created, cart is cleared                    #
    # ------------------------------------------------------------------ #
    order = store._checkout_processor.process_checkout(customer, cart, store._orders)
    order.update_status(OrderStatus.CONFIRMED)

    print("\n--- Order Confirmation ---")
    print(order)

    print(f"\nCart after checkout: {cart}")

    # ------------------------------------------------------------------ #
    #  4. Second customer places a separate order                          #
    # ------------------------------------------------------------------ #
    customer2 = Customer("C002", "Bob Johnson", "bob@example.com")
    cart2 = Cart()
    cart2.add_product(store.get_product("P001"))   # 1 × Laptop
    cart2.add_product(store.get_product("P003"), quantity=2)  # 2 × Keyboard

    order2 = store._checkout_processor.process_checkout(customer2, cart2, store._orders)
    order2.update_status(OrderStatus.SHIPPED)

    print("\n--- Second Order ---")
    print(order2)

    # ------------------------------------------------------------------ #
    #  5. Store order history                                              #
    # ------------------------------------------------------------------ #
    print(f"\n--- All Orders in Store ({len(store.get_all_orders())} total) ---")
    for o in store.get_all_orders():
        print(f"  Order #{o.order_id} | {o.customer.name} | {o.status.value} | ${o.grand_total:.2f}")

    # ------------------------------------------------------------------ #
    #  6. Stock after purchases                                            #
    # ------------------------------------------------------------------ #
    print("\n--- Remaining Stock ---")
    for p in store.list_products():
        print(f"  [{p.product_id}] {p.name}: {p.stock} left")


if __name__ == "__main__":
    main()

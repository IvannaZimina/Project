"""
main.py — Demo script for the Online Storefront project.

Run:  python main.py
"""

from store import Store
from cart import Cart
from customer import Customer
from factory import ProductFactory
from order import OrderStatus


def main():
    # ------------------------------------------------------------------ #
    #  1. Set up the store and populate the catalog via ProductFactory     #
    # ------------------------------------------------------------------ #
    store = Store("Python Online Storefront")

    store.add_product(ProductFactory.create(
        "physical", product_id="P001", name="Laptop",
        price=999.99, stock=10, weight_kg=2.5
    ))
    store.add_product(ProductFactory.create(
        "physical", product_id="P002", name="Wireless Headphones",
        price=79.99, stock=25, weight_kg=0.3
    ))
    store.add_product(ProductFactory.create(
        "physical", product_id="P003", name="Mechanical Keyboard",
        price=129.99, stock=15, weight_kg=1.1
    ))
    store.add_product(ProductFactory.create(
        "digital", product_id="D001", name="Python OOP Guide (eBook)",
        price=19.99, stock=100, download_url="https://store.example.com/dl/oop-guide"
    ))
    store.add_product(ProductFactory.create(
        "digital", product_id="D002", name="Web Development Course",
        price=49.99, stock=50, download_url="https://store.example.com/dl/webdev"
    ))

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
    order = store.checkout(customer, cart)
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

    order2 = store.checkout(customer2, cart2)
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

"""
tests/test_store.py — Unit tests for the Online Storefront project.

Run from the project root:
    python -m pytest tests/
  or
    python -m unittest discover tests/
"""

import sys
import os
import unittest

# Ensure the project root is on the path when running from the tests/ folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from product import PhysicalProduct, DigitalProduct
from cart import Cart, CartItem
from customer import Customer
from factory import ProductFactory
from store import Store
from order import Order, OrderStatus


# ===================================================================== #
#  Product tests                                                          #
# ===================================================================== #

class TestProduct(unittest.TestCase):

    def setUp(self):
        self.laptop = PhysicalProduct("P001", "Laptop", 999.99, 5, 2.5)
        self.ebook = DigitalProduct("D001", "Python Guide", 19.99, 100,
                                    "http://example.com/guide")

    def test_physical_shipping_cost(self):
        """Shipping = weight_kg * 2.50."""
        self.assertAlmostEqual(self.laptop.calculate_shipping(), 6.25)

    def test_digital_no_shipping(self):
        """Digital products always have zero shipping cost."""
        self.assertEqual(self.ebook.calculate_shipping(), 0.0)

    def test_price_setter_rejects_negative(self):
        """Setting a negative price must raise ValueError."""
        with self.assertRaises(ValueError):
            self.laptop.price = -1

    def test_reduce_stock_correct(self):
        """Stock decreases by the purchased quantity."""
        self.laptop.reduce_stock(2)
        self.assertEqual(self.laptop.stock, 3)

    def test_reduce_stock_insufficient_raises(self):
        """Buying more than available stock must raise ValueError."""
        with self.assertRaises(ValueError):
            self.laptop.reduce_stock(10)

    def test_get_info_contains_name(self):
        """get_info() output must include the product name."""
        self.assertIn("Laptop", self.laptop.get_info())
        self.assertIn("Python Guide", self.ebook.get_info())


# ===================================================================== #
#  Cart tests                                                             #
# ===================================================================== #

class TestCart(unittest.TestCase):

    def setUp(self):
        self.product = PhysicalProduct("P001", "Widget", 10.00, 20, 1.0)
        self.cart = Cart()

    def test_add_product_appears_in_cart(self):
        self.cart.add_product(self.product, 3)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].quantity, 3)

    def test_subtotal_calculation(self):
        self.cart.add_product(self.product, 4)
        self.assertAlmostEqual(self.cart.get_total(), 40.00)

    def test_shipping_total_calculation(self):
        """Shipping total = weight * 2.50 * quantity."""
        self.cart.add_product(self.product, 2)
        # 1.0 kg * 2.50 * 2 = 5.00
        self.assertAlmostEqual(self.cart.get_shipping_total(), 5.00)

    def test_grand_total_includes_shipping(self):
        self.cart.add_product(self.product, 1)
        expected = 10.00 + 2.50  # price + shipping (1 kg)
        self.assertAlmostEqual(self.cart.get_grand_total(), expected)

    def test_add_beyond_stock_raises(self):
        with self.assertRaises(ValueError):
            self.cart.add_product(self.product, 100)

    def test_remove_product(self):
        self.cart.add_product(self.product)
        self.cart.remove_product("P001")
        self.assertTrue(self.cart.is_empty())

    def test_remove_missing_product_raises(self):
        with self.assertRaises(ValueError):
            self.cart.remove_product("NONEXISTENT")

    def test_clear_empties_cart(self):
        self.cart.add_product(self.product, 5)
        self.cart.clear()
        self.assertTrue(self.cart.is_empty())

    def test_add_same_product_twice_accumulates(self):
        self.cart.add_product(self.product, 2)
        self.cart.add_product(self.product, 3)
        self.assertEqual(self.cart.items[0].quantity, 5)


# ===================================================================== #
#  Checkout & Order tests                                                 #
# ===================================================================== #

class TestCheckout(unittest.TestCase):

    def setUp(self):
        self.store = Store("Test Store")
        self.product = PhysicalProduct("P001", "Gadget", 50.00, 10, 0.5)
        self.store.add_product(self.product)
        self.customer = Customer("C001", "Test User", "test@example.com")
        self.cart = Cart()

    def test_checkout_returns_order(self):
        self.cart.add_product(self.product, 2)
        order = self.store.checkout(self.customer, self.cart)
        self.assertIsInstance(order, Order)

    def test_order_total_is_correct(self):
        self.cart.add_product(self.product, 2)
        order = self.store.checkout(self.customer, self.cart)
        self.assertAlmostEqual(order.total, 100.00)

    def test_order_default_status_is_pending(self):
        self.cart.add_product(self.product, 1)
        order = self.store.checkout(self.customer, self.cart)
        self.assertEqual(order.status, OrderStatus.PENDING)

    def test_checkout_reduces_stock(self):
        self.cart.add_product(self.product, 3)
        self.store.checkout(self.customer, self.cart)
        self.assertEqual(self.product.stock, 7)

    def test_checkout_clears_cart(self):
        self.cart.add_product(self.product, 1)
        self.store.checkout(self.customer, self.cart)
        self.assertTrue(self.cart.is_empty())

    def test_checkout_empty_cart_raises(self):
        with self.assertRaises(ValueError):
            self.store.checkout(self.customer, self.cart)

    def test_order_linked_to_customer(self):
        self.cart.add_product(self.product, 1)
        order = self.store.checkout(self.customer, self.cart)
        self.assertIn(order, self.customer.get_orders())

    def test_order_status_update(self):
        self.cart.add_product(self.product, 1)
        order = self.store.checkout(self.customer, self.cart)
        order.update_status(OrderStatus.SHIPPED)
        self.assertEqual(order.status, OrderStatus.SHIPPED)


# ===================================================================== #
#  ProductFactory tests                                                   #
# ===================================================================== #

class TestProductFactory(unittest.TestCase):

    def test_create_physical_returns_correct_type(self):
        p = ProductFactory.create("physical", product_id="X1", name="Box",
                                  price=5.00, stock=10, weight_kg=1.0)
        self.assertIsInstance(p, PhysicalProduct)

    def test_create_digital_returns_correct_type(self):
        d = ProductFactory.create("digital", product_id="X2", name="eBook",
                                  price=9.99, stock=999, download_url="http://dl.example.com")
        self.assertIsInstance(d, DigitalProduct)

    def test_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("unknown", product_id="X3", name="?",
                                  price=1.00, stock=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

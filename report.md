# OOP Project Design Report

**Student:** Ivanna Zimina  
**Project Title:** Online Storefront  
**Date:** 2026

---

## 1. Introduction

This project implements a simple online storefront application in Python. It allows customers to browse a product catalog, add items to a shopping cart, and complete a purchase that produces an order record. The system supports two categories of products: physical goods that require shipping, and digital goods that are delivered instantly by download.

The main features of the program are:
- A product catalog that can hold both physical and digital products.
- A shopping cart with add, remove, and clear operations.
- Shipping cost calculation that varies by product type.
- A checkout process that reduces stock and creates an order.
- Order status tracking (Pending → Confirmed → Shipped → Delivered).
- A factory for creating products without exposing construction details.
- A full suite of 26 unit tests.

---

## 2. Class Design

### List of Classes

| Class | File | Responsibility |
|---|---|---|
| `Product` | `product.py` | Abstract base class — defines the common interface for all products (name, price, stock, `get_info()`, `calculate_shipping()`). |
| `PhysicalProduct` | `product.py` | Concrete subclass — adds `weight_kg` and implements shipping at $2.50/kg. |
| `DigitalProduct` | `product.py` | Concrete subclass — adds `download_url`, shipping is always $0.00. |
| `CartItem` | `cart.py` | Pairs a product with a chosen quantity; computes the line subtotal. |
| `Cart` | `cart.py` | Holds a collection of `CartItem` objects; calculates totals and shipping. |
| `Customer` | `customer.py` | Stores customer data and keeps a personal order history. |
| `OrderStatus` | `order.py` | Enum — represents the lifecycle states of an order. |
| `Order` | `order.py` | Immutable record of a completed purchase; holds a snapshot of items and totals. |
| `ProductFactory` | `factory.py` | Factory — creates `PhysicalProduct` or `DigitalProduct` objects based on a type string. |
| `Store` | `store.py` | Manages the catalog and orchestrates the checkout process. |

### Relationships

- **Inheritance:** `PhysicalProduct` and `DigitalProduct` both inherit from the abstract class `Product`.
- **Composition:** `Cart` contains a collection of `CartItem` objects; each `CartItem` holds a reference to a `Product`.
- **Association:** `Store` operates on `Cart` and `Customer` objects during checkout, and creates `Order` objects. `Customer` holds references to its `Order` objects.
- **Dependency:** `ProductFactory` depends on `PhysicalProduct` and `DigitalProduct` to construct instances.

---

## 3. Application of OOP Principles

### Encapsulation
All instance attributes across every class are declared as private (prefixed with `_`). Access is provided only through `@property` getters, and where modification is allowed, through validated setters. For example, the `price` setter in `Product` raises a `ValueError` if a negative value is supplied, and the `quantity` setter in `CartItem` rejects values less than one. This prevents the internal state of any object from being corrupted by external code.

### Inheritance
`PhysicalProduct` and `DigitalProduct` both extend the abstract class `Product`. They inherit the common attributes (`product_id`, `name`, `price`, `stock`) and the `reduce_stock()` method without duplicating code. Each subclass only adds what is unique to it: `weight_kg` for physical products and `download_url` for digital ones. Both subclasses also override the two abstract methods to provide their own behaviour.

### Polymorphism
The two abstract methods `get_info()` and `calculate_shipping()` are overridden in each subclass. The rest of the application (for example, the shipping calculation loop in `Cart`) calls `product.calculate_shipping()` on any product without knowing whether it is physical or digital. The correct result is returned automatically based on the actual runtime type. This means new product types can be added in the future without changing `Cart` or `Store`.

### Abstraction
`Product` is declared as an abstract base class using Python's `abc.ABC` and the `@abstractmethod` decorator. It is impossible to instantiate `Product` directly. This forces every concrete product type to implement `get_info()` and `calculate_shipping()`, ensuring a consistent interface across the entire catalog. The rest of the program interacts with products only through this interface.

---

## 4. Use of Design Patterns

### Factory Pattern (`ProductFactory`)

`ProductFactory` in `factory.py` provides a single entry point for creating products. Client code calls `ProductFactory.create("physical", ...)` or `ProductFactory.create("digital", ...)` instead of calling the constructors directly. This hides construction details (e.g., which arguments belong to which class), makes it easy to add new product types in one place, and keeps the catalog-setup code in `main.py` uniform and readable.

---

## 5. SOLID Principles

### Single Responsibility Principle
Each class has exactly one reason to change. `Cart` is responsible only for managing the collection of items and calculating totals — it does not know about customers or orders. `Order` only stores the data of a completed purchase. `Store` is the only class that orchestrates the checkout flow. If the shipping formula changes, only `PhysicalProduct` needs to be updated. If the checkout steps change, only `Store` needs to be updated.

### Open/Closed Principle
The system is open for extension but closed for modification. Adding a new product type (for example, a `SubscriptionProduct`) requires only creating a new subclass of `Product` and a new branch in `ProductFactory.create()`. The existing classes `Cart`, `Store`, and `Order` do not need to change at all, because they interact with products through the `Product` interface (`calculate_shipping()`, `get_info()`, etc.).

---

## 6. Testing Strategy

All tests are located in `tests/test_store.py` and use Python's built-in `unittest` framework. Tests are grouped into four test classes that correspond to the main components of the application.

**Test classes and examples:**

| Test class | What is tested |
|---|---|
| `TestProduct` | Shipping cost formula, negative-price rejection, stock reduction, stock overflow. |
| `TestCart` | Adding items, subtotal and shipping totals, grand total, stock guard, remove item, clear cart, accumulating quantity. |
| `TestCheckout` | Order creation, correct total, default PENDING status, stock reduction after purchase, cart cleared after checkout, empty-cart guard, order linked to customer, status update. |
| `TestProductFactory` | Correct types returned for "physical" and "digital", `ValueError` for unknown type. |

Running all tests:
```
python -m pytest tests/ -v
```
Result: **26 passed**.

---

## 7. Challenges and Design Decisions

One design decision was where to place the checkout logic. It could have lived inside `Cart`, but that would mean the cart knows about customers and order storage — violating Single Responsibility. Placing it in `Store` keeps `Cart` a pure data structure and makes `Store` the single coordinator of the purchase flow.

Another decision was using a `CartItem` snapshot in `Order`. After checkout, the cart is cleared and stock is reduced. Storing a list of `CartItem` objects in the `Order` means the order record remains accurate even if those products are later removed from the catalog or their prices change.

The `OrderStatus` enum was chosen over plain strings to prevent typos and make status transitions explicit and easy to validate in the future.

---

## 8. Conclusion

The project successfully demonstrates all four OOP pillars in a realistic, small-scale scenario. Abstraction and polymorphism are combined through the `Product` hierarchy so that `Cart` and `Store` never need to distinguish between product types at runtime. Encapsulation protects all object state and keeps validation in one place. Inheritance eliminates code duplication between `PhysicalProduct` and `DigitalProduct`. The Factory pattern keeps object creation centralized, and the SOLID principles result in a design where classes have clear, focused responsibilities.

With more time, I would add a discount or coupon system (a good use case for the Decorator pattern), persist orders and customers to a file or database, and add an interactive command-line or web interface for browsing the catalog.

## 9. How to Run the Program
1. Ensure you have Python 3.8 or higher installed.
2. Clone the repository and navigate to the project directory.
3. Run the main program:
```python main.py
```
4. Follow the prompts to browse products, add to cart, and checkout.
5. To run the tests:
```python -m pytest tests/ -v
```
All tests should pass successfully.

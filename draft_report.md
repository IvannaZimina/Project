# OOP Project Design Report — Draft

**Student:** Ivanna Zimina
**Project Title:** Online Storefront
**Date:** March 15, 2026
**Language:** Python 3

---

## 1. Introduction

In this project, I built a small online store simulation. The flow is similar to a real e-commerce site: a customer can view products, add them to a cart, and check out. My goal was to create a small but complete example that shows how real objects (store, customer, cart, product) can be built as classes.

The main challenge is that products do not behave in the same way. Physical products need shipping, while digital products are delivered by link and have no shipping cost. I wanted one clean system that supports both types without repeating code.

**Who can use it and why:**
This project can help beginners in Python/OOP who want a clear and realistic example. It can also be a base for future pet-project for the portfolio.

**Main features implemented:**
- Product catalog containing both physical and digital products;
- Shopping cart: add items, remove items, view totals;
- Automatic shipping cost calculation based on product type;
- Checkout process: reduces stock, creates an order record;
- Order status tracking: Pending → Confirmed → Shipped → Delivered;

**Tools used:**
- Language: Python 3
- Standard library modules: `abc` (abstract base classes), `enum`, `datetime`
- No external frameworks required to run the core program

---

## 2. Class Design

### 2.1 List of Classes

| Class | File | Responsibility |
|---|---|---|
| `Product` | `product.py` | Abstract base class for all products. It defines common rules for every product type. |
| `PhysicalProduct` | `product.py` | Product type for items that need shipping. |
| `DigitalProduct` | `product.py` | Product type for downloadable items with no shipping. |
| `CartItem` | `cart.py` | One position in the cart: which product and how many pieces. |
| `Cart` | `cart.py` | Stores selected items and calculates totals for checkout. |
| `Customer` | `customer.py` | Represents a buyer and keeps their order history. |
| `OrderStatus` | `order.py` | Defines valid order states (pending, shipped, delivered, etc.). |
| `Order` | `order.py` | Stores completed purchase data created during checkout. |
| `Store` | `store.py` | Central class that manages catalog and performs checkout. |

### 2.2 Class Relationships

```
Product (ABC)
    |-- PhysicalProduct
    |-- DigitalProduct

Cart
    |-- contains --> CartItem
CartItem
    |-- references --> Product

Store
    |-- has catalog of --> Product
    |-- uses --> Cart
    |-- receives --> Customer
    |-- creates --> Order

Order
    |-- uses status --> OrderStatus
```

| Class A | Relation | Class B | Why this relation exists |
|---|---|---|---|
| `PhysicalProduct` | inherits from | `Product` | Reuses common product logic and overrides specific behavior. |
| `DigitalProduct` | inherits from | `Product` | Same base interface, different shipping behavior. |
| `Cart` | contains | `CartItem` | Cart is built from line items. |
| `CartItem` | references | `Product` | Each line item stores product + quantity. |
| `Store` | manages catalog of | `Product` | Store keeps all products in one place. |
| `Store` | uses | `Cart` | Checkout reads selected items from cart. |
| `Store` | receives | `Customer` | Checkout is done for a specific customer. |
| `Store` | creates | `Order` | Final result of checkout is a new order. |
| `Order` | uses | `OrderStatus` | Order state is controlled by enum values. |

This section shows both a simple structure diagram and a direct relation table, so it is easy to see not only what classes exist, but also how they interact.

### 2.3 Key Design Decisions

**Why `Product` is abstract:**
`PhysicalProduct` and `DigitalProduct` share common fields, but shipping works differently. So I made `Product` abstract: every new product type must implement `get_info()` and `calculate_shipping()`. Because of this, the rest of the code does not need `if product type ...` checks everywhere.

**Why `CartItem` is a separate class (not just a dictionary):**
I could store cart data as `{product: quantity}`, but then calculation logic would be spread across other places. With `CartItem`, one object keeps both data and behavior (for example, subtotal). This made cart code cleaner.

**Why `Order` stores a snapshot of items (not references):**
After checkout, the cart is cleared and product stock changes. If `Order` kept only live references, old orders could become incorrect later. That is why I store a snapshot at purchase time, so order history stays correct.

---

## 3. Application of OOP Principles

### 3.1 Encapsulation

In my classes, fields are **private** (`_field`) and are accessed through `@property`. When values can change, I use setters with validation.

Example — `price` in `Product`:

```python
@property
def price(self) -> float:
    return self._price

@price.setter
def price(self, value: float):
    if value < 0:
        raise ValueError("Price cannot be negative.")
    self._price = value
```

So, outside code cannot set a negative price. I use the same idea for `CartItem.quantity` (it cannot be less than 1). This keeps objects valid and avoids repeated checks in many places.

---

### 3.2 Inheritance

`PhysicalProduct` and `DigitalProduct` both inherit from `Product`. Common data and logic are written once in the parent class and reused by child classes.

```python
class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight_kg):
        super().__init__(product_id, name, price, stock)  # reuse parent __init__
        self._weight_kg = weight_kg
```

Each subclass adds only what is specific to it (`weight_kg` or `download_url`) and implements abstract methods in its own way. This reduces duplicated code and is easier to maintain.

---

### 3.3 Polymorphism

Both subclasses override `calculate_shipping()`. In `Cart`, I call this method for all products without checking the exact type:

```python
def get_shipping_total(self) -> float:
    return round(
        sum(item.product.calculate_shipping() * item.quantity
            for item in self._items.values()),
        2,
    )
```

For `PhysicalProduct`, shipping is based on weight. For `DigitalProduct`, shipping is `0.0`. The call is the same, but behavior is different depending on the object type. This is practical polymorphism.

The same idea works for `get_info()`: one method call, different output format for each product class.

---

### 3.4 Abstraction

I defined `Product` as an **abstract base class** using Python `abc`:

```python
from abc import ABC, abstractmethod

class Product(ABC):

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def calculate_shipping(self) -> float:
        pass
```

Because of `@abstractmethod`, Python will not allow direct creation of `Product()`:

```python
p = Product("P1", "Test", 5.0, 10)
# → TypeError: Can't instantiate abstract class Product
```

This is abstraction: the base class says what methods must exist, and subclasses define how they work. So the rest of the program uses one common interface (`get_info`, `calculate_shipping`) and does not depend on internal details.

---

### 3.5 Code Readability (Docstrings)

To make the code easier to read, I use triple-quoted strings `""" ... """` in classes and methods. These are called **docstrings**. They briefly explain what a class or method does.

Example:
```python
def get_orders(self) -> list:
    """Return a copy of the customer's orders."""
    return list(self._orders)
```
This helps quickly understand the purpose of the code without reading all implementation details.

---

## Classes Demonstrating Class Design and OOP Principles

| Class | Why it is relevant |
|---|---|
| `Product`, `PhysicalProduct`, `DigitalProduct` | Core example of abstraction, inheritance, and polymorphism ([product.py](product.py)). |
| `CartItem`, `Cart` | Show composition (`Cart` contains `CartItem`) and shipping polymorphism ([cart.py](cart.py)). |
| `Store` | Main coordinator class that connects catalog, cart, customer, and order flow ([store.py](store.py)). |
| `Customer` | Clear example of encapsulation and order history management ([customer.py](customer.py)). |
| `Order`, `OrderStatus` | Show order snapshot design and controlled status lifecycle ([order.py](order.py)). |

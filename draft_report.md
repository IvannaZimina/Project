# OOP Project Design Report — Draft

**Student:** Ivanna Zimina
**Project Title:** Online Storefront
**Date:** March 15, 2026
**Language:** Python 3

---

## 1. Introduction

This project is a simulation of a simple online storefront. It models a typical e-commerce scenario where a customer can browse a catalog of products, add items to a shopping cart, and complete a purchase. The goal was to build a small but complete system that shows how real-world objects — a store, a customer, a cart, a product — can be represented as classes in code.

The problem the project addresses is straightforward: in a real online shop, different types of products (physical and digital) behave differently. A physical product has weight and needs to be shipped; a digital product is delivered by download at no extra cost. The system needs to handle both types through the same interface, without duplicating logic.

**Who can use it and why:**
Any student or developer learning OOP can use this project as a reference for how to structure a multi-class Python application. It is also a clear example of how abstract classes, inheritance, and encapsulation work together in a practical setting.

**Main features implemented:**
- Product catalog containing both physical and digital products
- Shopping cart: add items, remove items, view totals
- Automatic shipping cost calculation based on product type
- Checkout process: reduces stock, creates an order record
- Order status tracking: Pending → Confirmed → Shipped → Delivered

**Tools used:**
- Language: Python 3
- Standard library modules: `abc` (abstract base classes), `enum`, `datetime`
- No external frameworks required to run the core program

---

## 2. Class Design

### 2.1 List of Classes

| Class | File | Responsibility |
|---|---|---|
| `Product` | `product.py` | **Abstract base class.** Defines the shared interface for all products: `product_id`, `name`, `price`, `stock`, `reduce_stock()`, `get_info()`, `calculate_shipping()`. Cannot be instantiated on its own. |
| `PhysicalProduct` | `product.py` | Extends `Product`. Adds `weight_kg`. Implements shipping as $2.50 per kilogram. |
| `DigitalProduct` | `product.py` | Extends `Product`. Adds `download_url`. Shipping cost is always $0.00. |
| `CartItem` | `cart.py` | Pairs a `Product` with a quantity chosen by the customer. Calculates the line subtotal (price × quantity). |
| `Cart` | `cart.py` | Holds a dictionary of `CartItem` objects. Provides `add_product()`, `remove_product()`, `clear()`, and methods to compute the total, shipping total, and grand total. |
| `Customer` | `customer.py` | Stores the customer's ID, name, and email. Keeps a list of their completed orders. |
| `OrderStatus` | `order.py` | An `Enum` that defines the valid states of an order: PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED. |
| `Order` | `order.py` | Created at checkout. Stores a snapshot of the purchased items, totals, customer reference, and current status. |
| `Store` | `store.py` | Manages the product catalog. Runs the checkout: validates the cart, reduces stock, creates the `Order`, and links it to the customer. |

### 2.2 Class Relationships

```
                    ┌──────────────────┐
                    │    Product (ABC) │
                    │  - product_id    │
                    │  - name          │
                    │  - price         │
                    │  - stock         │
                    │  + get_info()    │  ← abstract
                    │  + calculate_    │  ← abstract
                    │    shipping()    │
                    └────────┬─────────┘
                             │  inherits
               ┌─────────────┴──────────────┐
               ▼                            ▼
  ┌─────────────────────┐      ┌──────────────────────┐
  │  PhysicalProduct    │      │   DigitalProduct     │
  │  - weight_kg        │      │   - download_url     │
  │  + calculate_       │      │   + calculate_       │
  │    shipping()→$/kg  │      │     shipping()→ $0   │
  └─────────────────────┘      └──────────────────────┘

  ┌────────────┐   contains   ┌───────────────┐
  │   Cart     │ ────────────▶│   CartItem    │
  │            │              │  - product    │◀── references Product
  │            │              │  - quantity   │
  └─────┬──────┘              └───────────────┘
        │ used by
        ▼
  ┌───────────────────────────────────────┐
  │              Store                    │
  │  - catalog (dict of Products)         │
  │  + checkout(customer, cart) → Order   │
  └──────────────────┬────────────────────┘
                     │ creates
                     ▼
              ┌─────────────┐      ┌───────────────┐
              │    Order    │◀─────│   Customer    │
              │  - items[]  │      │  - orders[]   │
              │  - status   │      └───────────────┘
              └─────────────┘
```

### 2.3 Key Design Decisions

**Why `Product` is abstract:**
Both `PhysicalProduct` and `DigitalProduct` share a lot of common data (name, price, stock), but their shipping logic is completely different. Making `Product` an abstract base class forces every new product type to implement `get_info()` and `calculate_shipping()`. This way the rest of the program never needs to check which type a product is — it just calls the method and gets the right answer.

**Why `CartItem` is a separate class (not just a dictionary):**
A dictionary like `{product: quantity}` would work for storing items, but it cannot hold behaviour (such as calculating its own subtotal). A `CartItem` object owns its product and quantity, and handles its own calculation. This keeps the logic where the data is.

**Why `Order` stores a snapshot of items (not references):**
After checkout the cart is cleared and stock is reduced. If `Order` stored only references to products, and those products were later removed from the catalog, the order record would become invalid. Storing a copy of the cart items at the moment of purchase keeps order history reliable.

---

## 3. Application of OOP Principles

### 3.1 Encapsulation

All attributes in every class are declared as **private** (prefixed with `_`). They are exposed to the outside world only through `@property` getters. Where the value can be changed, a setter with validation is provided.

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

No external code can set a negative price. The same pattern is applied to `quantity` in `CartItem`: setting it below 1 raises an error immediately. This means the objects always hold valid data — the validation is done once, inside the class, not scattered around the program.

---

### 3.2 Inheritance

`PhysicalProduct` and `DigitalProduct` both inherit from `Product`. The shared attributes (`product_id`, `name`, `price`, `stock`) and the shared method `reduce_stock()` are defined once in the parent class and reused automatically by both children.

```python
class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight_kg):
        super().__init__(product_id, name, price, stock)  # reuse parent __init__
        self._weight_kg = weight_kg
```

Each subclass then only adds what is specific to it (`weight_kg` or `download_url`) and provides its own implementation of the abstract methods. This eliminates duplication: if the stock-reduction logic needs to change, it changes in one place (`Product`), not in every product class.

---

### 3.3 Polymorphism

Both subclasses override `calculate_shipping()` with different behaviour. `Cart` calls this method on every product in the cart without ever checking the type:

```python
def get_shipping_total(self) -> float:
    return round(
        sum(item.product.calculate_shipping() * item.quantity
            for item in self._items.values()),
        2,
    )
```

When the item is a `PhysicalProduct`, `calculate_shipping()` returns `weight_kg * 2.50`. When it is a `DigitalProduct`, it returns `0.0`. The same one line of code produces the correct result for both types at runtime. This is polymorphism: the same call, different behaviour depending on the actual object.

The same applies to `get_info()` — it is called the same way for every product in `Store.display_catalog()`, but each subclass produces a different formatted string.

---

### 3.4 Abstraction

`Product` is defined as an **abstract base class** using Python's `abc` module:

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

The `@abstractmethod` decorator means Python will refuse to create a `Product()` object directly:

```python
p = Product("P1", "Test", 5.0, 10)
# → TypeError: Can't instantiate abstract class Product
```

This is abstraction: the base class defines *what* every product must be able to do, without specifying *how*. The "how" is the responsibility of each concrete subclass. The rest of the application only needs to know about the interface (`get_info`, `calculate_shipping`), not the internal details of any specific product type.

---

## Files recommended for the intermediate submission

| File | Why it is relevant |
|---|---|
| [product.py](product.py) | Shows abstraction, inheritance, encapsulation, and polymorphism all in one file — the most important file for demonstrating OOP. |
| [cart.py](cart.py) | Shows how `CartItem` encapsulates product+quantity, and how `Cart` uses polymorphism via `calculate_shipping()`. |
| [store.py](store.py) | Shows how objects collaborate: `Store` uses `Cart`, `Customer`, and creates `Order`. |
| [customer.py](customer.py) | Simple but clean example of encapsulation. |
| [order.py](order.py) | Shows use of `Enum` for order status and a snapshot design decision. |
| [main.py](main.py) | Demonstrates the full flow end-to-end — good to run live during a defence. |

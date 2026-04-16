# OOP Project Design Report - Online StoreFront

**Student:** Ivanna Zimina  
**Project Title:** Online Storefront  
**Date:** 2026

---

## 1. Introduction

I built a small online store simulation where a customer can view products, add them to a cart, and check out. The goal was a clear OOP example with both physical and digital products in one clean system.
**Main features:**
- Product catalog (physical + digital);
- Shopping cart with totals;
- Checkout that reduces stock and creates orders;
- Order status tracking (Pending -> Confirmed -> Shipped -> Delivered).

## 2. Class Design

### 2.1 List of Classes

| Class | Responsibility |
|---|---|
| `Product` | Abstract base class for all products. It defines common rules for every product type. |
| `PhysicalProduct` | Product type for items that need shipping. |
| `DigitalProduct` | Product type for downloadable items with no shipping. |
| `CartItem` | One position in the cart: which product and how many pieces. |
| `Cart` | Stores selected items and calculates totals for checkout. |
| `Customer` | Represents a buyer and keeps their order history. |
| `OrderStatus` | Defines valid order states (pending, shipped, delivered, etc.). |
| `Order` | Stores completed purchase data created during checkout. |
| `Store` | Central class that manages catalog and performs checkout. |
| `CheckoutProcessor` | Handles the checkout process, including stock reduction and order creation. |
| `InventoryManager` | Manages the store's product inventory. |
| `OrderManager` | Manages the store's order history and order retrieval. |

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
  |-- delegates checkout to --> CheckoutProcessor
  |-- uses --> InventoryManager
  |-- uses --> OrderManager

Order
  |-- uses status --> OrderStatus
```

| Class A | Relation | Class B | Why this relation exists |
|---|---|---|---|
| `PhysicalProduct`, `DigitalProduct` | inherit from | `Product` | Same base interface, different behavior. |
| `Cart` | contains | `CartItem` | Cart is built from line items. |
| `CartItem` | references | `Product` | Each line item stores product + quantity. |
| `Store` | coordinates | `Product`, `Cart`, `Customer`, `Order`, `CheckoutProcessor`, `InventoryManager`, `OrderManager` | Central coordinator of catalog and checkout. |
| `Order` | uses | `OrderStatus` | Order state is controlled by enum values. |

This section shows both a simple structure diagram and a direct relation table, so it is easy to see not only what classes exist, but also how they interact.

### 2.3 Key Design Decisions

**Why `Product` is abstract:**
`PhysicalProduct` and `DigitalProduct` share common fields, but shipping works differently. So I made `Product` abstract: every new product type must implement `get_info()` and `calculate_shipping()`.

**Why `CartItem` is a separate class (not just a dictionary):**
I could store cart data as `{product: quantity}`, but then calculation logic would be spread across other places. With `CartItem`, one object keeps both data and behavior (for example, subtotal).

**Why `Order` stores a snapshot of items (not references):**
After checkout, the cart is cleared and product stock changes. If `Order` kept only live references, old orders could become incorrect later. 

## 3. Application of OOP Principles

### 3.1 Encapsulation

In my classes, fields are **private** (`_field`) and are accessed through `@property`. When values can change, I use setters with validation.

Example - `price` in `Product`:

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
  def calculate_shipping(self) -> float:
    pass
```

Because of `@abstractmethod`, Python will not allow direct creation of `Product()`:

```python
p = Product("P1", "Test", 5.0, 10)
# -> TypeError: Can't instantiate abstract class Product
```

This is abstraction: the base class says what methods must exist, and subclasses define how they work. So the rest of the program uses one common interface (`get_info`, `calculate_shipping`) and does not depend on internal details.

---

### NB! Code Readability (Docstrings)

To make the code easier to read, I use triple-quoted strings `""" ... """` in classes and methods. These are called **docstrings**. They briefly explain what a class or method does.

Example:
```python
def get_orders(self) -> list:
  """Return a copy of the customer's orders."""
  return list(self._orders)
```
This helps quickly understand the purpose of the code without reading all implementation details.

---

## 4. Use of Design Patterns

### Factory Pattern (`ProductFactory`)

`ProductFactory` in `factory.py` is a small helper class for creating products. In `main.py`, I do not call `PhysicalProduct(...)` or `DigitalProduct(...)` directly. Instead, I call `ProductFactory.create(...)`, and the factory decides which product class to use based on the type.
This makes makes future changes simpler - if I want to add a new product type later, I only need to update the factory instead of changing many parts of the program.

---

## 5. SOLID Principles

### 5.1 Single Responsibility Principle
Each class has exactly one reason to change:
- `Cart` is responsible only for managing the collection of items and calculating totals — it does not know about customers or orders.
- `Order` only stores the data of a completed purchase.
- `Store` is the only class that orchestrates the checkout flow. If the shipping formula changes, only `PhysicalProduct` needs to be updated. If the checkout steps change, only `Store` needs to be updated.

### 5.2 Open/Closed Principle
The system is open for extension but closed for modification:
- Adding a new product type (e.g., `SubscriptionProduct`) requires only creating a new subclass of `Product` and a new branch in `ProductFactory.create()`.
- The existing classes `Cart`, `Store`, and `Order` do not need to change at all, because they interact with products through the `Product` interface (`calculate_shipping()`, `get_info()`, etc.).

---

## 6. Testing Strategy

I tested the core behaviors for `Product` and `Cart` using Python's built-in `unittest` framework. The assertion methods used in tests are summarized in `tests/unittest_assertions.md`. Example checks include shipping cost calculation and cart totals. Result: **7 passed**.

---

## 7. Challenges and Design Decisions

1. `Store` should not contain all business logic. I moved checkout, inventory, and order management into separate classes, so `Store` stays a coordinator that connects catalog, cart, customer, and services.
2. `Order` stores a snapshot of items because after checkout the cart is cleared and prices or stock can change, but order history must stay correct.
3. `OrderStatus` is an enum to avoid typos and keep states clear.

---

## 8. Conclusion

1. I applied core OOP ideas: encapsulation, inheritance, polymorphism, abstraction.
2. The `Product` hierarchy avoids type checks and keeps shipping logic clean.
3. The Factory pattern keeps product creation in one place; classes stay focused.


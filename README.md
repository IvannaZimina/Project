## OOP Project - Online StoreFront

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
- Order status tracking: Pending -> Confirmed -> Shipped -> Delivered;

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
  def get_info(self) -> str:
    pass

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
3. Run the main program: **python main.py**
4. Follow the prompts to browse products, add to cart, and checkout.
5. To run the tests: **python -m pytest tests/ -v**
All tests should pass successfully.

## Expected output in Console
```
=======================================================
  Python Online Storefront — Product Catalog
=======================================================
  [P001] [Physical] Laptop | Price: $999.99 | Weight: 2.5 kg | Stock: 10
  [P002] [Physical] Wireless Headphones | Price: $79.99 | Weight: 0.3 kg | Stock: 25
  [P003] [Physical] Mechanical Keyboard | Price: $129.99 | Weight: 1.1 kg | Stock: 15
  [D001] [Digital]  Python OOP Guide (eBook) | Price: $19.99 | Download: https://store.example.com/dl/oop-guide
  [D002] [Digital]  Web Development Course | Price: $49.99 | Download: https://store.example.com/dl/webdev
=======================================================

Customer: Alice Smith | Email: alice@example.com

Shopping Cart:
  Wireless Headphones x2 = $159.98
  Python OOP Guide (eBook) x1 = $19.99
  Web Development Course x1 = $49.99
  Subtotal : $229.96
  Shipping : $1.50
  Grand Total: $231.46

--- Order Confirmation ---
Order #1
  Customer  : Alice Smith
  Status    : Confirmed
  Date      : 2026-03-15 20:07
  Items:
    - Wireless Headphones x2 = $159.98
    - Python OOP Guide (eBook) x1 = $19.99
    - Web Development Course x1 = $49.99
  Subtotal  : $229.96
  Shipping  : $1.50
  Grand Total: $231.46

Cart after checkout: Cart is empty.

--- Second Order ---
Order #2
  Customer  : Bob Johnson
  Status    : Shipped
  Date      : 2026-03-15 20:07
  Items:
    - Laptop x1 = $999.99
    - Mechanical Keyboard x2 = $259.98
  Subtotal  : $1259.97
  Shipping  : $11.75
  Grand Total: $1271.72

--- All Orders in Store (2 total) ---
  Order #1 | Alice Smith | Confirmed | $231.46
  Order #2 | Bob Johnson | Shipped | $1271.72

--- Remaining Stock ---
  [P001] Laptop: 9 left
  [P002] Wireless Headphones: 23 left
  [P003] Mechanical Keyboard: 13 left
  [D001] Python OOP Guide (eBook): 99 left
  [D002] Web Development Course: 49 left
  ```


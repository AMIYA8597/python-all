"""
## A. Concept Name
Object-Oriented Programming (OOP) in Python

## B. One-Sentence Definition
OOP is a programming paradigm that organizes software design around data, or objects, rather than functions and logic, bundling related properties and behaviors into a single cohesive unit.

## C. Why Does This Exist?
As software grew in size and complexity in the 1970s and 1980s, procedural programming (just writing a long list of functions and global variables) became unmaintainable spaghetti code. State (data) and behavior (functions) were disconnected. If you changed a variable, you broke a dozen functions. OOP exists to solve the "complexity and state management" problem by modularizing code into self-contained "objects" that protect their own state and expose only safe ways to interact with it.

## D. Intuition
Think of writing code like running a restaurant.
Procedural code: Everyone shares one massive ledger. The chef, the waiter, and the manager are all writing in the same book, constantly overwriting each other's notes.
OOP code: Every employee is an "object." The Waiter knows their own orders. The Chef knows their own ingredients. You don't mess with the Chef's ingredients; you *ask* the Chef to cook a meal. 

## E. Real-Life Analogy
A Blueprint vs. A House.
- Class: The architectural blueprint. It defines that a house has 4 walls, a roof, and an open() method for the door.
- Object (Instance): The actual physical house built at 123 Main St. You can build millions of objects from one Class blueprint.
- State (Attributes): This specific house is painted blue.
- Behavior (Methods): Ringing the doorbell.

## F. Mental Model
In memory, a Class is a dictionary of functions (methods). An Object is a dictionary of data (attributes) plus a hidden pointer back to its Class. When you call `my_car.drive()`, Python translates it to `Car.drive(my_car)`.

## G. Visual Explanation
```text
[ Blueprint: CLASS 'BankAccount' ]
    |-- Attributes: owner_name, balance
    |-- Methods: deposit(), withdraw()
          |
          | (Instantiation: bank_account = BankAccount("Alice", 100))
          V
[ Instance: OBJECT 1 ]                 [ Instance: OBJECT 2 ]
    |-- owner_name: "Alice"                |-- owner_name: "Bob"
    |-- balance: $100                      |-- balance: $500
    |-- (Points to BankAccount methods)    |-- (Points to BankAccount methods)
```

## H. Formal Explanation
Object-Oriented Programming relies on four main pillars:
1. Encapsulation: Bundling data and methods that work on that data within one unit, restricting direct access to some of the object's components (using property setters/getters).
2. Abstraction: Hiding complex implementation details and showing only the essential features of the object.
3. Inheritance: A mechanism where a new class derives properties and characteristics from an existing class, promoting code reuse.
4. Polymorphism: The ability of different objects to respond in their own way to the same method call (e.g., `animal.speak()` does something different for a Dog vs. a Cat).

## I. Mathematical Foundation (if applicable)
OOP concepts map loosely to abstract algebra and set theory. 
- A Class is a Set `C`.
- An Object `x` is an element of `C` (`x ∈ C`).
- Inheritance implies subsets: If `Dog` inherits from `Animal`, then the set of all Dogs is a subset of the set of all Animals (`D ⊆ A`). Therefore, any function defined over `A` is applicable to elements in `D` (Liskov Substitution Principle).

## J. From-Scratch Implementation (if applicable)
See the Python code below the docstring for a full implementation demonstrating the four pillars of OOP (Encapsulation, Abstraction, Inheritance, and Polymorphism) using a mock Machine Learning Base Model and Neural Network Layer structure.

## K. Library / Production Implementation (if applicable)
In standard Python, `pathlib.Path` or `datetime.datetime` are excellent examples of production OOP. They encapsulate state (the file path string or the time data) and provide methods to interact with it (e.g., `path.exists()`, `dt.strftime()`), hiding the OS-level complexity.

## L. Trace (walk through example)
Let's trace `model = LinearRegression()` followed by `model.predict(100)` (using the code below):
1. `LinearRegression.__init__()` is called.
2. It hits `super().__init__("Linear Regression")`.
3. Execution jumps to `BaseModel.__init__()`, setting `self.name = "Linear Regression"` and `self.is_trained = False`.
4. Execution returns to `LinearRegression.__init__()`, setting `self.coef = 0.5`.
5. We call `model.train([])`. Python looks for `train` in `LinearRegression`. Doesn't find it.
6. Python looks up the MRO (Method Resolution Order) and finds `train` in `BaseModel`.
7. `BaseModel.train()` sets `self.is_trained = True`.
8. We call `model.predict(100)`. Python finds `predict` in `LinearRegression`.
9. `self.is_trained` is True. It returns `100 * 0.5 = 50.0`.

## M. Complexity
- Time Complexity of Instantiation: O(1) mostly, just allocating memory and pointing variables.
- Space/Memory: 
  - Each Class object takes memory once (stores the method pointers).
  - Each Instance takes memory for its internal dictionary `__dict__` which holds its attributes.
  - Python uses `__slots__` (an advanced concept) if you need to optimize memory by preventing the creation of `__dict__` for millions of objects.
- Method Lookup Time: O(1) amortized. Python uses C3 linearization and aggressively caches method resolution orders.

## N. Common Mistakes
1. Mutable Default Arguments in Class definition:
   `class A: items = []` 
   If you append to `items`, ALL instances of A share the exact same list. 
   Fix: Initialize lists inside `__init__`.
2. Forgetting `self`: 
   Writing `def my_method():` instead of `def my_method(self):`. Python will throw an error saying it takes 0 positional arguments but 1 was given.
3. Overusing Inheritance: Deep inheritance trees (e.g., A inherits from B inherits from C inherits from D) make code impossible to trace. Favor "Composition over Inheritance".

## O. Common Confusions
- Class Attribute vs. Instance Attribute: 
  Class attributes are shared by ALL objects (like a company policy). Instance attributes belong ONLY to the specific object (like an employee's salary).
- `__init__` vs `__new__`:
  `__new__` is what actually creates and allocates memory for the object. `__init__` simply initializes the state *after* it's been created. You rarely override `__new__` unless building a Singleton or metaprogramming.
- Single Underscore `_var` vs Double Underscore `__var`:
  `_var` is just a gentleman's agreement meaning "please don't touch this from outside". 
  `__var` triggers "Name Mangling". Python renames it to `_ClassName__var` to prevent accidental overriding in subclasses. Do not use `__var` just for privacy.

## P. When To Use
- When state and behavior are inherently linked (e.g., A User object that holds user data and has a `.login()` method).
- When you have many variations of a concept that share identical interfaces (e.g., Different ML models sharing `.train()` and `.predict()`).
- Building large-scale applications (GUI applications, games, complex simulations).

## Q. When NOT To Use
- Simple scripts or data transformation pipelines. Use pure functions instead.
- Math-heavy transformations (Data Science/ETL) often favor functional programming concepts (map, filter, reduce) over object-oriented ones.
- When it forces unnecessary abstraction (creating a `StringPrinterManagerFactory` just to print a string).

## R. Trade-offs
- **Pros**: Encourages modularity, makes large codebases manageable, allows code reuse via inheritance and polymorphism. Maps well to real-world modeling.
- **Cons**: Overhead of writing boilerplate code (classes, init methods). Can lead to overly complex architectures (e.g., deep inheritance hierarchies) and hidden state mutations that make debugging difficult if not careful.

## S. Debugging
- Issue: "AttributeError: 'MyClass' object has no attribute 'x'"
  Fix: Ensure `self.x` is initialized in `__init__`. Also check if you misspelled it or forgot `self.`.
- Issue: Changing an attribute on one object changes it for ALL objects.
  Fix: You defined it at the class level instead of inside `__init__`. Move it to `self.var = ...` inside `__init__`.
- Use `dir(obj)` or `obj.__dict__` to see exactly what attributes an object currently has at runtime.

## T. Memory Hook (a short memorable principle)
"Classes are cookie cutters. Objects are the cookies. Methods are what you can do to the cookie. Attributes are the chocolate chips inside."

## U. Active Recall (questions before answers)
1. What does the `self` keyword represent?
2. Why is getter/setter (property) better than letting users directly modify an attribute like `obj.weight = -5`?
3. What is the difference between overriding a method and inheriting it?
4. What happens if you define `my_list = []` directly under `class Test:` instead of in `__init__`?

## V. Practice (exercises)
Exercise: Create a `BankAccount` class. It should have a private `_balance`, a `deposit(amount)` method, and a `withdraw(amount)` method. 
If withdrawal exceeds balance, raise a ValueError. Add a class attribute `bank_name` set to "GlobalBank".

Solution:
```python
class BankAccount:
    bank_name = "GlobalBank"
    
    def __init__(self, initial_balance: float = 0.0):
        self._balance = initial_balance
        
    @property
    def balance(self) -> float:
        return self._balance
        
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        
    def withdraw(self, amount: float):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
```

## W. Interview Question
Q: "Explain Polymorphism and give a real-world software example where it significantly improves code maintainability."
A: Polymorphism allows objects of different classes to be treated as objects of a common superclass. It means "many forms." 
Example: A payment processing system. You have an interface `PaymentGateway` with a `.process_payment(amount)` method. You have subclasses `StripeGateway`, `PayPalGateway`, and `CryptoGateway`. The checkout logic just loops over the selected gateway and calls `.process_payment(amount)`. If tomorrow we add `ApplePayGateway`, the core checkout loop code doesn't change AT ALL. It adheres to the Open-Closed Principle.

## X. Project Connection
In deep learning frameworks like PyTorch, OOP is the backbone. Every neural network you build inherits from `torch.nn.Module`. 
You override the `__init__` to define your layers (state), and you override the `forward()` method to define the computation (behavior). 
PyTorch relies heavily on polymorphism and encapsulation to auto-calculate gradients seamlessly in the background without exposing the terrifying calculus to the developer!
"""

import math
from typing import List, Type, Dict, Any

# ==========================================
# From-Scratch Implementation
# ==========================================

# Let's implement a system demonstrating all 4 pillars of OOP.

# Pillar 1 & 2: Abstraction & Encapsulation
class NeuralNetworkLayer:
    """
    A class representing a single layer in a neural network.
    Demonstrates Encapsulation (hiding weights) and Abstraction (exposing simple forward pass).
    """
    
    # Class Attribute: Shared across all instances
    layer_count = 0 
    
    def __init__(self, input_size: int, output_size: int, activation: str):
        # Instance Attributes: Unique to each instance
        self.input_size = input_size
        self.output_size = output_size
        self.activation = activation
        
        # 'Protected' attribute (convention: single leading underscore)
        # We don't want outside code randomly altering the weights matrix.
        self._weights: List[List[float]] = self._initialize_weights()
        
        NeuralNetworkLayer.layer_count += 1
        
    def _initialize_weights(self) -> List[List[float]]:
        """Private method (abstraction): The user doesn't need to know how weights are init'd."""
        # Mock initialization with 0.1 for simplicity
        return [[0.1 for _ in range(self.input_size)] for _ in range(self.output_size)]
    
    @property
    def weights(self) -> List[List[float]]:
        """Getter: Safely read the weights."""
        return self._weights
    
    @weights.setter
    def weights(self, new_weights: List[List[float]]):
        """Setter (encapsulation): Validates new data before allowing a state change."""
        if len(new_weights) != self.output_size or len(new_weights[0]) != self.input_size:
            raise ValueError("Weight matrix dimensions do not match layer sizes.")
        self._weights = new_weights
        
    def forward(self, inputs: List[float]) -> List[float]:
        """The public API. Abstracting away the math."""
        # Mock forward pass
        return [sum(w * i for w, i in zip(node_weights, inputs)) for node_weights in self._weights]


# Pillar 3: Inheritance
class BaseModel:
    """Base class providing shared functionality for all ML Models."""
    
    def __init__(self, name: str):
        self.name = name
        self.is_trained = False
        
    def train(self, data: List[Any]):
        print(f"Training {self.name} base logic...")
        self.is_trained = True
        
    def predict(self, data: Any):
        raise NotImplementedError("Subclasses must implement the predict method.")


# Pillar 4: Polymorphism
class LinearRegression(BaseModel):
    def __init__(self):
        super().__init__("Linear Regression")
        self.coef = 0.5
        
    def predict(self, data: float) -> float:
        # Polymorphic behavior specific to Linear Regression
        if not self.is_trained:
            raise RuntimeError("Model not trained.")
        return data * self.coef

class DecisionTree(BaseModel):
    def __init__(self):
        super().__init__("Decision Tree")
        
    def predict(self, data: float) -> float:
        # Polymorphic behavior specific to Decision Tree
        if not self.is_trained:
            raise RuntimeError("Model not trained.")
        return 1.0 if data > 10 else 0.0


# Let's see it in action
def demonstrate_polymorphism(models: List[BaseModel], test_data: float):
    """
    This function accepts any BaseModel. It doesn't care if it's a Tree or a Regression.
    Because of Polymorphism, calling `.predict()` does the right thing for each object.
    """
    for model in models:
        model.train([])
        result = model.predict(test_data)
        print(f"{model.name} prediction for {test_data}: {result}")


if __name__ == "__main__":
    print("Running OOP Demonstrations...")
    layer = NeuralNetworkLayer(input_size=3, output_size=2, activation='relu')
    print("Initial weights:", layer.weights)
    print("Forward pass with [1.0, 0.5, -1.0]:", layer.forward([1.0, 0.5, -1.0]))
    
    print("\nDemonstrating Polymorphism:")
    models = [LinearRegression(), DecisionTree()]
    demonstrate_polymorphism(models, 15.0)
    print("\nOOP Mastery Complete!")

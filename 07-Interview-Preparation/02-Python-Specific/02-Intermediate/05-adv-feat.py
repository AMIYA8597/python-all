"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - ADVANCED FEATURES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I want to build a Python web framework like Django. How do I 
# mathematically intercept the creation of a Class before it even exists in RAM, 
# so I can automatically register it in a global database?"
#
# You cannot do this with `__init__` or `__new__` (which intercept Object creation).
# You must intercept CLASS creation using a Metaclass! A Metaclass is the "Class 
# of a Class". Just as an Object is an instance of a Class, a Class is an instance 
# of a Metaclass.
#
# Interviewer: "How does the `@property` decorator actually work under the hood?"
# It uses the Descriptor Protocol (`__get__`, `__set__`). If you master Descriptors, 
# you understand how Python fundamentally routes attribute access.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Metaclasses (Intercepting Class definition).
# - Master the Descriptor Protocol (Custom Attribute Routing).
# - Master Structural Pattern Matching (Python 3.10+ `match`).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. METACLASSES (THE CLASS FACTORY)
# ==============================================================================
# A global registry for our web framework!
REGISTRY = {}

class RegistryMeta(type):
    """
    A Metaclass MUST inherit from `type`.
    This `__new__` fires at Compile Time (when the Python script is read), 
    NOT at Runtime (when an object is instantiated).
    """
    def __new__(mcs, name, bases, namespace):
        print(f"  [METACLASS] Intercepting the creation of Class '{name}'...")
        
        # We can dynamically inject attributes into the class before it exists!
        namespace['injected_by_meta'] = "Framework Magic"
        
        # Physically create the class using the core C-level `type` allocator
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Automatically register it!
        if name != "BaseModel":
            REGISTRY[name] = cls
            
        return cls

class BaseModel(metaclass=RegistryMeta):
    pass

class User(BaseModel):
    pass

class Post(BaseModel):
    pass

def demonstrate_metaclasses():
    section_header("Metaclasses (Intercepting Class Creation)")
    
    print("Notice that the Metaclass print statements fired BEFORE this function ")
    print("even executed! They fired when the module was imported.\n")
    
    print("Checking the Global Registry:")
    print(f"  {REGISTRY}")
    print("\nDid the Metaclass successfully inject attributes?")
    
    u = User()
    print(f"  u.injected_by_meta: '{u.injected_by_meta}'")


# ==============================================================================
# 4. DESCRIPTORS (OVERRIDING ATTRIBUTE ACCESS)
# ==============================================================================
class ValidatedString:
    """
    A Descriptor. Any attribute assigned this class will automatically route 
    all GET and SET operations through these dunder methods!
    """
    def __set_name__(self, owner, name):
        # Automatically captures the name of the variable it was assigned to!
        self.public_name = name
        self.private_name = '_' + name
        
    def __get__(self, obj, objtype=None):
        print(f"  [DESCRIPTOR GET] Accessing {self.public_name}...")
        return getattr(obj, self.private_name, None)
        
    def __set__(self, obj, value):
        print(f"  [DESCRIPTOR SET] Validating {self.public_name}...")
        if not isinstance(value, str):
            raise TypeError(f"{self.public_name} MUST be a string!")
        if len(value) < 3:
            raise ValueError(f"{self.public_name} is too short!")
            
        # Store it on the parent object!
        setattr(obj, self.private_name, value)

class Person:
    # We assign the Descriptor to the class level!
    name = ValidatedString()
    job = ValidatedString()

def demonstrate_descriptors():
    section_header("Descriptors (The Magic behind @property)")
    
    p = Person()
    
    print("Attempting to set `p.name = 'Alice'`:")
    p.name = "Alice"
    
    print("\nAttempting to get `p.name`:")
    val = p.name
    print(f"Result: {val}")
    
    print("\nAttempting to bypass validation: `p.job = 123`")
    try:
        p.job = 123
    except TypeError as e:
        print(f"  [CRASH PREVENTED] {e}")


# ==============================================================================
# 5. STRUCTURAL PATTERN MATCHING (PYTHON 3.10+)
# ==============================================================================
def route_api_request(request: dict):
    """
    A massive switch statement on steroids. It doesn't just match Values; 
    it matches the mathematical STRUCTURAL SHAPE of the dictionary!
    """
    match request:
        case {"status": 200, "data": {"user": str(name)}}:
            # It matched the structure AND automatically extracted the name!
            print(f"  [Match] Success! Welcome, {name}.")
            
        case {"status": int(code), "error": str(err)} if code >= 500:
            # Guard clause using `if`
            print(f"  [Match] FATAL SERVER ERROR {code}: {err}")
            
        case {"status": 404}:
            print("  [Match] Not Found.")
            
        case _: # The catch-all wildcard
            print("  [Match] Unknown payload structure.")

def demonstrate_pattern_matching():
    section_header("Structural Pattern Matching (Python 3.10+)")
    
    payload_1 = {"status": 200, "data": {"user": "Alice"}}
    print(f"Payload: {payload_1}")
    route_api_request(payload_1)
    
    payload_2 = {"status": 503, "error": "Database Timeout"}
    print(f"\nPayload: {payload_2}")
    route_api_request(payload_2)


def run_all_labs():
    demonstrate_metaclasses()
    demonstrate_descriptors()
    demonstrate_pattern_matching()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the physical difference between an Object, a Class, and a Metaclass?"
   Senior Answer: "An Object is an instance of a Class. A Class is a physical blueprint stored in RAM that defines how that Object behaves. However, in Python, *everything is an object, including Classes themselves*. Therefore, a Class must be an instance of something else! That 'something else' is a Metaclass (specifically, the built-in C-level `type`). Just as `__new__` in a Class intercepts the physical creation of an Object, `__new__` in a Metaclass intercepts the physical creation of the Class itself. This allows frameworks like Django ORM to scan your Class for fields and automatically generate SQL tables before a single Object is ever instantiated."

2. Interviewer: "How does the `@property` decorator actually work? Where does the function go?"
   Senior Answer: "The `@property` decorator is simply a built-in implementation of the Descriptor Protocol. When you decorate a method with `@property`, Python replaces that method with a Descriptor object that implements the `__get__` dunder method. When a user types `obj.my_property`, Python detects that `my_property` is not a raw value, but a Descriptor. It mathematically halts the standard dictionary lookup, and reroutes the request by executing the Descriptor's `__get__` method, which dynamically calculates and returns the value on the fly."

3. Interviewer: "Why is Python 3.10's `match/case` mathematically superior to a giant `if/elif` chain?"
   Senior Answer: "An `if/elif` chain forces you to manually perform tedious type-checking, dictionary key validation, and variable extraction sequentially (e.g., `if 'data' in req and 'user' in req['data'] and isinstance(req['data']['user'], str): name = req['data']['user']`). This is brittle and unreadable. `match/case` is 'Structural Pattern Matching'. It allows you to declare a complex mathematical shape as a template. The CPython engine uses highly optimized internal C-code to simultaneously validate the existence of keys, verify the data types, and unpack the variables into local scope in a single, lightning-fast operation."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Advanced Features) Completed.")

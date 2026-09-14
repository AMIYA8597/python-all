"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - THE ORM ARCHITECTURE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Build a mini Django Object-Relational Mapper (ORM) from scratch."
#
# This is the ultimate test of Python mastery. To build an ORM, you must combine 
# everything: Descriptors, Metaclasses, and advanced dunder methods.
# 
# You need Descriptors to intercept `user.age = 25` and ensure it is an Integer, 
# and maybe even trigger a SQL `UPDATE` behind the scenes.
# You need a Metaclass to intercept `class User(Model):` and dynamically generate 
# a SQL `CREATE TABLE Users` string before the object is ever instantiated.
#
# You also must absolutely understand the horrific difference between `__getattr__` 
# and `__getattribute__`. Mixing them up will crash your program with an 
# Infinite Recursion `RecursionError` instantly.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a production-grade Django-style ORM using Metaclasses + Descriptors.
# - Master `__getattr__` (Fallback) vs `__getattribute__` (Absolute Intercept).
# - Understand the Infinite Recursion Trap.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BUILDING A MINI ORM (DESCRIPTORS + METACLASSES)
# ==============================================================================

# --- 1. The Descriptor (The Fields) ---
class IntegerField:
    """A Descriptor that forces an attribute to be a strictly typed integer."""
    def __init__(self, primary_key=False):
        self.primary_key = primary_key
        
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = '_' + name
        
    def __get__(self, obj, objtype=None):
        if obj is None: return self # Accessed via class
        return getattr(obj, self.private_name, None)
        
    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"Database Error: {self.name} MUST be an Integer!")
        setattr(obj, self.private_name, value)

class StringField:
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = '_' + name
        
    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.private_name, None)
        
    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"Database Error: {self.name} MUST be a String!")
        setattr(obj, self.private_name, value)


# --- 2. The Metaclass (The Table Generator) ---
class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        # We don't want to process the base 'Model' class itself!
        if name == "Model":
            return super().__new__(mcs, name, bases, namespace)
            
        print(f"  [ORM METACLASS] Scanning '{name}' for Database Fields...")
        
        # We mathematically extract all the Descriptors the user defined!
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, (IntegerField, StringField)):
                fields[key] = value
                
        # Inject the parsed fields directly into the Class definition!
        namespace['_database_fields'] = fields
        namespace['_table_name'] = name.lower() + "s"
        
        # Automatically generate the SQL CREATE TABLE query!
        sql_cols = []
        for f_name, f_type in fields.items():
            db_type = "INT" if isinstance(f_type, IntegerField) else "VARCHAR(255)"
            pk = " PRIMARY KEY" if getattr(f_type, 'primary_key', False) else ""
            sql_cols.append(f"{f_name} {db_type}{pk}")
            
        sql = f"CREATE TABLE {namespace['_table_name']} ({', '.join(sql_cols)});"
        namespace['creation_sql'] = sql
        
        return super().__new__(mcs, name, bases, namespace)

# --- 3. The Base Class ---
class Model(metaclass=ModelMeta):
    def save(self):
        """Simulates saving the instance to the database."""
        # We iterate over the Metaclass-injected fields to generate an INSERT query!
        cols = []
        vals = []
        for f_name in self._database_fields.keys():
            cols.append(f_name)
            # Use the descriptor to get the validated value
            val = getattr(self, f_name) 
            vals.append(f"'{val}'" if isinstance(val, str) else str(val))
            
        sql = f"INSERT INTO {self._table_name} ({', '.join(cols)}) VALUES ({', '.join(vals)});"
        print(f"  [ORM SAVE] Executing: {sql}")


# --- 4. The User Code! ---
class Employee(Model):
    id = IntegerField(primary_key=True)
    name = StringField()
    age = IntegerField()

def demonstrate_orm():
    section_header("Building an ORM (Metaclasses + Descriptors)")
    
    print("1. Did the Metaclass automatically generate the SQL schema at compile time?")
    print(f"   Generated SQL: {Employee.creation_sql}")
    
    print("\n2. Instantiating a new Employee...")
    e = Employee()
    
    print("3. Validating data using Descriptors...")
    e.id = 1
    e.name = "Alice"
    e.age = 30
    
    print("   Attempting to inject a string into an IntegerField...")
    try:
        e.age = "Thirty"
    except TypeError as err:
        print(f"   [CRASH PREVENTED] {err}")
        
    print("\n4. Triggering the dynamic save()...")
    e.save()


# ==============================================================================
# 4. __GETATTR__ VS __GETATTRIBUTE__ (THE RECURSION TRAP)
# ==============================================================================
class DangerousObject:
    def __init__(self):
        self.real_data = "Hello"
        
    def __getattr__(self, item):
        """
        THE FALLBACK.
        This ONLY fires if the attribute physically DOES NOT EXIST in the dictionary.
        It is extremely safe to use.
        """
        return f"Fallback for missing attribute: {item}"

class TerrifyingObject:
    def __init__(self):
        self.real_data = "Hello"
        
    def __getattribute__(self, item):
        """
        THE ABSOLUTE INTERCEPT.
        This fires for EVERY SINGLE attribute access, even if it exists!
        """
        print(f"  [Intercepted] Accessing {item}...")
        
        # FATAL FLAW! 
        # If we try to return self.real_data here, Python sees `self.real_data`.
        # `self.real_data` triggers `__getattribute__` again!
        # Which prints, and then calls `self.real_data`, which triggers `__getattribute__`...
        # Infinite Recursion. The stack blows up instantly.
        
        # The ONLY way to escape is to call the ultimate C-level object allocator:
        return super().__getattribute__(item)

def demonstrate_getattribute():
    section_header("__getattr__ vs __getattribute__")
    
    print("Testing `__getattr__` (The Fallback)...")
    safe = DangerousObject()
    print(f"  Accessing existing: {safe.real_data}")
    print(f"  Accessing missing : {safe.fake_data}")
    
    print("\nTesting `__getattribute__` (The Absolute Intercept)...")
    scary = TerrifyingObject()
    print(f"  Accessing existing: {scary.real_data}")
    print("  Notice that it intercepted the call, but safely escaped using `super()`!")


def run_all_labs():
    demonstrate_orm()
    demonstrate_getattribute()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In our ORM, why did we need the Metaclass? Why couldn't we just generate the `CREATE TABLE` SQL inside the `__init__` method of the Employee class?"
   Senior Answer: "The `__init__` method only runs when an Object is *instantiated* (e.g., `e = Employee()`). If you are running database migrations, you don't want to instantiate fake objects just to figure out what the schema should be! You need the class structure to be evaluated and the SQL to be generated mathematically at *compile time* (when the module is first imported). The Metaclass intercepts the physical definition of the `Employee` class itself, parses its attributes, and generates the `CREATE TABLE` string as a Class Attribute. This allows a migration script to simply read `Employee.creation_sql` without ever creating an object."

2. Interviewer: "I wrote a `__getattribute__` method, and the moment I instantiate the class, I get a `RecursionError: maximum recursion depth exceeded`. What did I do?"
   Senior Answer: "You fell into the Infinite Recursion Trap. `__getattribute__` is absolute; it intercepts literally *every* attribute lookup on the object, including lookups originating from inside `__getattribute__` itself! If you wrote `return self.__dict__[item]` inside the method, the act of looking up `self.__dict__` triggers `__getattribute__` again, which looks up `self.__dict__`, triggering it again, spiraling infinitely until the C-stack blows up. To safely access attributes inside `__getattribute__`, you MUST bypass the object's interception layer entirely by delegating to the base C-class: `super().__getattribute__(item)`."

3. Interviewer: "What is the physical sequence of events when I write `user.age` on an ORM model?"
   Senior Answer: "1. Python checks the Object's `__getattribute__`. 
   2. It sees that `age` points to a Descriptor object attached to the Class. 
   3. Because the Descriptor protocol takes precedence over the instance dictionary, it halts the standard lookup and reroutes execution to the Descriptor's `__get__` dunder method. 
   4. The `__get__` method receives the `user` instance, mathematically looks up the hidden private variable (e.g., `user._age`), and returns it to the caller. This invisible routing is the core magic of Python frameworks."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Advanced ORM Architecture) Completed.")

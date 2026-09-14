"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (WEB DEVELOPMENT - DJANGO & ORM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer uses Flask to build a massive E-Commerce platform. They 
# spend 6 months manually writing raw SQL queries, building custom password 
# hashing algorithms, and designing an Admin dashboard from scratch. They get 
# hacked due to a SQL Injection vulnerability they missed on line 14,000.
#
# A senior engineer understands "Monoliths". They install `Django`. In 15 minutes, 
# they define the Database Models in pure Python. Django automatically generates 
# cryptographically secure SQL schema migrations, provides a military-grade 
# authentication system, and physically auto-generates a complete, beautiful 
# Admin UI out of thin air. They ship to Production 6 months faster.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the architecture of the Django ORM (Object-Relational Mapper).
# - Understand Model definitions, QuerySets, and Lazy Evaluation.
# - Differentiate the structural philosophy of Django vs Flask.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DJANGO ORM ARCHITECTURE (SIMULATED)
# ==============================================================================
# Django relies on massive project directories (`manage.py`, `settings.py`). 
# We cannot boot a full Django server in a single script easily, so we will 
# mathematically simulate the ORM architecture to understand the design pattern!

class DjangoModelSimulation:
    """Simulates the base `django.db.models.Model` class."""
    objects = None # In reality, this is the 'Manager' that executes SQL.

class CharField:
    def __init__(self, max_length): self.max_length = max_length
class DecimalField:
    def __init__(self, max_digits, decimal_places): pass
class ForeignKey:
    def __init__(self, to, on_delete): pass

# --- 1. DEFINING THE SCHEMA IN PURE PYTHON ---
# In Django, you NEVER write "CREATE TABLE User (id INT...)"!
# You write a Python Class. Django mathematically translates this class into 
# raw PostgreSQL, MySQL, or SQLite bytecode during 'Migrations'.

class User(DjangoModelSimulation):
    username = CharField(max_length=50)
    email = CharField(max_length=255)

class Order(DjangoModelSimulation):
    # The Foreign Key creates a mathematically perfect SQL JOIN relationship!
    # on_delete=CASCADE means if the User is deleted, all their orders die too.
    user = ForeignKey(User, on_delete="CASCADE")
    total_price = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(max_length=20)


# ==============================================================================
# 4. LAZY EVALUATION (THE QUERYSET)
# ==============================================================================
def demonstrate_lazy_evaluation():
    section_header("The Django ORM: QuerySets and Lazy Evaluation")
    
    print("  [SCENARIO] We want to find all 'PENDING' orders over $100.")
    
    print("\n  [JUNIOR APPROACH: RAW SQL]")
    print("    sql = \"SELECT * FROM orders WHERE status='PENDING' AND total_price > 100\"")
    print("    cursor.execute(sql)")
    print("    (Prone to SQL Injection, not portable across DB engines.)")
    
    print("\n  [SENIOR APPROACH: THE DJANGO ORM]")
    print("    pending_orders = Order.objects.filter(status='PENDING', total_price__gt=100)")
    
    print("\n  [CRITICAL ARCHITECTURE: LAZY EVALUATION]")
    print("    When you run `Order.objects.filter(...)`, Django executes EXACTLY ZERO SQL queries!")
    print("    It mathematically constructs a 'QuerySet' (a Python object that represents the query).")
    print("    It waits until the absolute last millisecond (e.g., when you loop over the data,")
    print("    or serialize it to JSON) before physically hitting the database.")
    
    print("\n    Example:")
    print("    q = Order.objects.filter(status='PENDING')           # DB Hits: 0")
    print("    q = q.exclude(user__username='admin')                # DB Hits: 0")
    print("    q = q.order_by('-total_price')                       # DB Hits: 0")
    print("    ")
    print("    for order in q:                                      # DB Hits: 1 (Combined SQL execution!)")
    print("        print(order.total_price)")
    
    print("\n  [CONCLUSION] Lazy Evaluation allows developers to chain complex logic together")
    print("  without destroying the database with hundreds of partial queries.")


# ==============================================================================
# 5. THE N+1 QUERY PROBLEM
# ==============================================================================
def demonstrate_n_plus_one():
    section_header("The N+1 Query Problem (The Silent ORM Killer)")
    
    print("  [SCENARIO] We want to print every Order, and the User's email who placed it.")
    
    print("\n  [THE CATASTROPHIC MISTAKE]")
    print("    orders = Order.objects.all()")
    print("    for order in orders:")
    print("        print(order.total_price, order.user.email)")
    
    print("\n    -> Database Hit 1: SELECT * FROM orders; (Gets 1,000 orders)")
    print("    -> Database Hit 2: SELECT * FROM users WHERE id = 1; (Inside loop!)")
    print("    -> Database Hit 3: SELECT * FROM users WHERE id = 2; (Inside loop!)")
    print("    ... repeats 1,000 times!")
    print("    Total Queries: 1001. The server crashes from I/O latency.")
    
    print("\n  [THE DJANGO SOLUTION (select_related)]")
    print("    orders = Order.objects.select_related('user').all()")
    print("    for order in orders:")
    print("        print(order.total_price, order.user.email)")
    
    print("\n    -> Database Hit 1: SELECT * FROM orders INNER JOIN users ON ...;")
    print("    Total Queries: 1. The framework mathematically resolves the Foreign")
    print("    Key at the SQL level, loading all data into RAM simultaneously!")


def run_all_labs():
    demonstrate_lazy_evaluation()
    demonstrate_n_plus_one()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is an ORM (Object-Relational Mapper), and how does it prevent SQL Injection?"
   Senior Answer: "An ORM translates raw SQL databases into pure Python Objects. Instead of writing `SELECT * FROM users`, you write `User.objects.all()`. When a user submits an HTTP form containing a malicious string like `admin'; DROP TABLE users;--`, a naive raw SQL `f-string` concatenation would physically execute the drop command, destroying the database. An ORM mathematically sanitizes and escapes all inputs using Parameterized Queries at the C-level Database Driver. The malicious string is strictly treated as a literal text value (`'admin\\'; DROP TABLE...'`), permanently immunizing the application against $100\\%$ of SQL Injection vectors without any manual developer intervention."

2. Interviewer: "Explain 'Lazy Evaluation' in the context of a Django QuerySet."
   Senior Answer: "When you execute a method like `.filter()` or `.exclude()` on a Django Model, the framework mathematically refuses to touch the Database. It returns a `QuerySet` object, which is merely a programmatic AST (Abstract Syntax Tree) representing the *intent* to query. You can chain $50$ filters together, and the Database I/O is exactly zero. The framework waits for the exact millisecond the data is 'evaluated' (e.g., iterating in a `for` loop, printing it, or casting it to a `list()`). At that exact moment, the ORM compiles the entire chain of 50 filters into a *single, highly-optimized SQL statement*. This prevents the application from making $50$ sequential round-trips over the network."

3. Interviewer: "What is the 'N+1 Query Problem', and how do you resolve it in Django?"
   Senior Answer: "The N+1 problem occurs when an ORM fetches a list of Parent records (1 query), and then, inside a `for` loop, accesses a Child relationship for each record (N queries). If you fetch 5,000 Orders, and then print `order.user.email` inside the loop, the ORM mathematically executes 1 initial query for the orders, and 5,000 subsequent queries to fetch each user. 5,001 network round-trips to the Database will catastrophically crash the web request latency. In Django, you resolve this by appending `.select_related('user')` (for Foreign Keys) or `.prefetch_related()` (for Many-to-Many). This mathematically alters the SQL compiler to execute an `INNER JOIN`, pulling all parent and child data into Python RAM in exactly $1$ query, eliminating the N loops."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Web Development (Django & ORM) Completed.")

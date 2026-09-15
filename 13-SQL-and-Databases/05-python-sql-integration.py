"""
# ==============================================================================
# LABORATORY: SQL & DATABASES (PYTHON-SQL INTEGRATION & ORMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes raw SQL strings across 500 files in their codebase. 
# One day, the company mandates switching from PostgreSQL to MySQL. Because 
# raw SQL syntax varies slightly between engines (e.g., RETURNING vs LAST_INSERT_ID), 
# the junior developer must manually rewrite 500 files. They miss 10 queries, 
# and the application crashes in Production.
#
# A senior software engineer uses an ORM (Object-Relational Mapper) like SQLAlchemy. 
# They define their Database Schema using pure Python Classes (Objects). The ORM 
# acts as a mathematical translator. When the engineer calls `session.add(user)`, 
# the ORM automatically compiles the precise SQL dialect for the target Database Engine. 
# To switch from Postgres to MySQL, the engineer changes exactly 1 line of configuration 
# code. The 500 files mathematically remain untouched.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the SQLAlchemy ORM Architecture.
# - Execute Data Mapping between Python Objects and SQL Tables.
# - Architect Database Connection Pooling for high concurrency.
# - Understand the N+1 Query Problem in ORMs.
#
# ==============================================================================
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE ARCHITECTURE (THE ORM DEFINITION)
# ==============================================================================
# The Declarative Base is a Metaclass that automatically converts these Python 
# classes into mathematical SQL CREATE TABLE statements!
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    # We define SQL Columns as Class Attributes!
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    
    # We define the Python relationship (Not an actual SQL column!)
    # This tells SQLAlchemy to mathematically JOIN the tables when we ask for `user.posts`
    posts = relationship("Post", back_populates="author")
    
    def __repr__(self):
        return f"<User(name='{self.username}')>"


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id')) # Foreign Key!
    
    author = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(title='{self.title}')>"


# ==============================================================================
# 4. THE BUSINESS LOGIC (EXECUTION)
# ==============================================================================
class ORMSimulator:
    
    def __init__(self, db_url: str = "sqlite:///orm_lab.db"):
        # The Engine is the core connection point.
        # We set `echo=True` so we can mathematically observe the raw SQL being generated!
        self.engine = create_engine(db_url, echo=False)
        
        # The Session is the "Workspace" (Transaction scope).
        self.Session = sessionmaker(bind=self.engine)
        
        # This mathematically executes all the CREATE TABLE commands!
        Base.metadata.drop_all(self.engine) # Clean slate
        Base.metadata.create_all(self.engine)
        
    def execute_workflow(self):
        session = self.Session()
        
        print("  [ORM] 1. Creating Objects (No SQL executed yet)...")
        # Notice we are just instantiating normal Python objects!
        alice = User(username="alice_arch")
        post1 = Post(title="Understanding B-Trees")
        post2 = Post(title="SQLAlchemy Patterns")
        
        # We link them together using pure Python lists!
        alice.posts.extend([post1, post2])
        
        print("  [ORM] 2. Adding to Session (Still no SQL executed)...")
        session.add(alice)
        
        print("  [ORM] 3. Committing to Database (SQL is generated and executed!)...")
        # The ORM translates the Python objects into INSERT INTO statements!
        session.commit()
        
        print("\n  [ORM] 4. Querying the Database (SQL SELECT translated to Python Objects)...")
        # We query the Python Class, not the table string!
        queried_user = session.query(User).filter_by(username="alice_arch").first()
        
        print(f"    -> Found User: {queried_user}")
        print(f"    -> Accessing Posts (Triggers a Lazy Load / JOIN!):")
        for post in queried_user.posts:
            print(f"       - {post.title}")
            
        session.close()


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_orm():
    section_header("SQL Integration: SQLAlchemy ORM")
    
    sim = ORMSimulator()
    sim.execute_workflow()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By utilizing an ORM, we mathematically abstracted the SQL syntax. ")
    print("  We interacted with pure Python classes, and the ORM engine generated ")
    print("  the perfect SQL Dialect under the hood, guaranteeing absolute syntax ")
    print("  safety and cross-database portability.")
    
    # Cleanup
    if os.path.exists("orm_lab.db"):
        os.remove("orm_lab.db")


def run_all_labs():
    demonstrate_orm()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the N+1 Query Problem in ORMs, and how do you mathematically solve it?"
   Senior Answer: "Lazy Loading Catastrophe. By default, ORMs use 'Lazy Loading'. If you query $100$ Users (`session.query(User).all()`), the ORM executes $1$ SQL query. Then, if you write a `for user in users: print(user.posts)` loop in Python, the ORM detects you are asking for the posts, which it hasn't fetched yet. It executes $1$ new SQL query *per user* to fetch their posts. The result is $1 + 100 = 101$ SQL queries hitting the Database over the network, causing massive latency. You solve this mathematically via 'Eager Loading' (`.options(joinedload(User.posts))`), forcing the ORM to compile a single massive `LEFT JOIN` and pull all the data into RAM using exactly $1$ query."

2. Interviewer: "Why would an Enterprise Application use a Connection Pool instead of opening a new Database connection for every HTTP Request?"
   Senior Answer: "TCP Handshake and Authentication Overhead. Opening a physical TCP socket to a Database server, negotiating TLS encryption, and authenticating the username/password takes approximately $20-50$ milliseconds. If an API receives $1,000$ requests per second, and creates a new connection for each one, the Database CPU will mathematically choke on authentication overhead alone. A Connection Pool (e.g., SQLAlchemy's `QueuePool`) boots up $10$ connections when the app starts, keeps them permanently alive, and simply hands them out to API requests as needed. When the request finishes, the connection is returned to the pool, achieving $O(1)$ connection latency."

3. Interviewer: "If ORMs are so powerful and prevent SQL Injection automatically, why do some Senior Engineers still choose to write raw SQL for specific endpoints?"
   Senior Answer: "Complex Analytical Aggregation (OLAP). An ORM is mathematically optimized for OLTP (Online Transaction Processing) — doing rapid CRUD operations on single rows (e.g., updating a user's password). However, if you need to run an aggressive financial report that `JOINS` 8 tables, applies 3 Window Functions, and uses `GROUPING SETS`, the ORM's abstraction layer will either generate wildly inefficient SQL, or it will be impossible to express the logic in pure Python syntax. For these specific, hyper-optimized analytical endpoints, Senior Engineers bypass the ORM and execute parameterized Raw SQL to guarantee maximum C++ execution efficiency."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: SQL Integration (ORM) Completed.")

"""
# ==============================================================================
# LABORATORY: SYMBOLIC MATHEMATICS (SYMPY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Thus far, every library we have used in Python performs NUMERIC mathematics. 
# If you ask Python for `math.sqrt(8)`, it executes the hardware floating-point 
# approximation and returns `2.8284271247461903`.
#
# If you are doing Engineering or Pure Mathematics, this approximation is unacceptable. 
# You don't want a decimal. You want the exact algebraic representation: `2 * sqrt(2)`.
#
# SymPy (Symbolic Python) is a Computer Algebra System (CAS) written entirely 
# in Python. It does not calculate decimals. It manipulates mathematical 
# EQUATIONS and SYMBOLS natively.
#
# It can analytically factor massive polynomials, solve systems of algebraic 
# equations, compute exact limits, and even perform exact analytical Calculus 
# (Derivatives and Integrals) yielding equations as output, not numbers!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Define Symbolic Variables (`symbols`).
# - Perform Algebraic manipulation (Expand, Factor, Simplify).
# - Perform Analytical Calculus (Derivatives and Definite/Indefinite Integrals).
# - Solve Algebraic Equations.
#
# ==============================================================================
"""

import sympy as sp

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EXACT REPRESENTATIONS & SYMBOLS
# ==============================================================================
def demonstrate_symbols():
    section_header("Exact Symbolic Representation")
    
    # Standard Python Evaluation (Numeric approximation)
    print(f"Standard Python sqrt(8): {8**0.5}")
    
    # SymPy Evaluation (Exact Symbolic Math)
    # `sp.sqrt` returns an un-evaluated mathematical object!
    exact_root = sp.sqrt(8)
    print(f"SymPy exact sqrt(8)    : {exact_root}")
    
    # We must explicitly declare letters as abstract Mathematical Symbols!
    # Without this, Python would just throw a NameError complaining 'x is not defined'.
    x, y = sp.symbols('x y')
    
    # Now we can build abstract equations!
    equation = x + 2*y + x - y
    print(f"\nAbstract Equation: {equation}")
    print("Notice how SymPy automatically combines like terms: (x + x) and (2y - y)!")


# ==============================================================================
# 4. ALGEBRAIC MANIPULATION
# ==============================================================================
def demonstrate_algebra():
    section_header("Algebraic Manipulation")
    
    x = sp.symbols('x')
    
    # 1. EXPANDING
    # Let's expand a massive binomial: (x + 3)^4
    binomial = (x + 3)**4
    expanded = sp.expand(binomial)
    print(f"Original : {binomial}")
    print(f"Expanded : {expanded}")
    
    # 2. FACTORING
    # Let's reverse the process! We give it a chaotic polynomial and ask for the roots.
    polynomial = x**3 - 6*x**2 + 11*x - 6
    factored = sp.factor(polynomial)
    print(f"\nPolynomial : {polynomial}")
    print(f"Factored   : {factored} -> (The roots are 1, 2, and 3!)")
    
    # 3. SIMPLIFICATION
    # SymPy will aggressively use trigonometric identities to collapse equations!
    trig_eq = sp.sin(x)**2 + sp.cos(x)**2
    simplified = sp.simplify(trig_eq)
    print(f"\nTrigonometric Identity: {trig_eq}")
    print(f"Simplified            : {simplified}")


# ==============================================================================
# 5. ANALYTICAL CALCULUS
# ==============================================================================
def demonstrate_calculus():
    section_header("Analytical Calculus (Derivatives & Integrals)")
    
    x = sp.symbols('x')
    
    # We define a function: f(x) = sin(x) * e^x
    func = sp.sin(x) * sp.exp(x)
    print(f"Original Function f(x): {func}")
    
    # 1. DERIVATIVES
    # Using the Product Rule automatically!
    derivative = sp.diff(func, x)
    print(f"\nDerivative f'(x)      : {derivative}")
    
    # 2. INDEFINITE INTEGRALS (Anti-derivatives)
    integral = sp.integrate(func, x)
    print(f"\nIndefinite Integral   : {integral} + C")
    
    # 3. DEFINITE INTEGRALS (Area under the curve)
    # Let's calculate the exact area under a parabola: f(x) = x^2 from x=0 to x=3.
    parabola = x**2
    # Syntax: (function, (variable, start, end))
    area = sp.integrate(parabola, (x, 0, 3))
    print(f"\nExact Area under x^2 from 0 to 3: {area} (Mathematically perfect 9)")
    
    # 4. LIMITS
    # Let's compute the famous limit: sin(x)/x as x approaches 0.
    limit_func = sp.sin(x) / x
    exact_limit = sp.limit(limit_func, x, 0)
    print(f"\nLimit of (sin(x)/x) as x->0 : {exact_limit}")


# ==============================================================================
# 6. SOLVING EQUATIONS
# ==============================================================================
def demonstrate_solvers():
    section_header("Solving Algebraic Equations")
    
    x, y = sp.symbols('x y')
    
    # 1. SOLVING A QUADRATIC EQUATION
    # By default, sp.solve assumes the expression equals 0.
    # Solve: x^2 - x - 2 = 0
    quad = x**2 - x - 2
    roots = sp.solve(quad, x)
    print(f"Roots of {quad} = 0 : {roots}")
    
    # 2. SOLVING A SYSTEM OF LINEAR EQUATIONS
    # Equation 1: x + y = 10
    # Equation 2: x - y = 2
    # To use sp.solve, we must rewrite them to equal 0!
    # eq1 -> x + y - 10 = 0
    # eq2 -> x - y - 2 = 0
    eq1 = x + y - 10
    eq2 = x - y - 2
    
    system_solution = sp.solve((eq1, eq2), (x, y))
    print(f"\nSystem of Equations:")
    print(f"1) x + y = 10")
    print(f"2) x - y = 2")
    print(f"Solution: {system_solution}")


def run_all_labs():
    demonstrate_symbols()
    demonstrate_algebra()
    demonstrate_calculus()
    demonstrate_solvers()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between NumPy and SymPy?
   Answer: NumPy is a NUMERICAL engine. It executes raw $C$-level hardware arithmetic on massive matrices of floating-point numbers. If you ask NumPy for the roots of a polynomial, it will return an array of decimal approximations. 
   SymPy is a SYMBOLIC engine (Computer Algebra System). It manipulates abstract mathematical equations without ever evaluating them as numbers. If you ask SymPy for the roots, it will return the exact algebraic fractions (e.g., $1/3$, or $\sqrt{2}$). NumPy is for Data Science. SymPy is for Pure Mathematics and Engineering.

2. Why must we explicitly define `x = sp.symbols('x')`?
   Answer: In standard Python, if you write the equation `result = x + 5`, the Python Interpreter immediately looks for a variable named `x` in the current memory scope. If it doesn't find a variable with a physical numerical value, it throws a `NameError` and crashes. By declaring `sp.symbols`, we are injecting a special object into Python's memory that intercepts all mathematical operators (`+`, `-`, `*`), preventing Python from trying to evaluate the math, and instead building an abstract mathematical syntax tree!

3. In `sp.solve()`, why do we rewrite equations to equal zero?
   Answer: The standard mathematical syntax for root-finding algorithms inherently searches for intercepts on the X-axis (where $y = 0$). While you can construct explicit Equality objects in SymPy (`sp.Eq(x + y, 10)`), it is significantly faster and standard practice to algebraically subtract the right side of the equation to the left side (`x + y - 10`), leaving an implicit zero on the right. The solver engine exclusively operates on expressions assumed to equal zero.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: SymPy Symbolic Math Completed.")

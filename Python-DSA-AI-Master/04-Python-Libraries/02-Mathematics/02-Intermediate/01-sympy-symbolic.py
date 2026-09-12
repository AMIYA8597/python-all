"""
Module: 01-sympy-symbolic
Description: Comprehensive textbook-grade interactive lesson on Symbolic Mathematics using SymPy.

===============================================================================
                           PYTHON DSA AI MASTER
                       SYMBOLIC MATHEMATICS WITH SYMPY
===============================================================================

Learning Objectives:
1. Understand the core concepts of Computer Algebra Systems (CAS) and SymPy.
2. Master symbolic variable creation, expression manipulation, and substitution.
3. Perform calculus operations: Limits, Derivatives, Integrals, and Series Expansions.
4. Solve complex algebraic and differential equations (ODEs) symbolically.
5. Explore Matrix operations and Linear Algebra symbolically.
6. Analyze performance considerations (Big-O) of symbolic vs. numerical computation.
7. Apply symbolic math to real-world physics and algorithmic problems.

Mathematical Background:
Unlike numerical computation libraries (e.g., NumPy) which use floating-point 
approximations, symbolic computation (Computer Algebra Systems) treats variables 
algebraically. For example, calculating the square root of 8 numerically yields 
2.8284271247461903, but symbolically it yields `2*sqrt(2)`. This preserves 
mathematical exactness, avoids floating-point truncation errors, and enables 
the derivation of exact analytical solutions to equations, integrals, and limits.

Performance Analysis & Big-O:
- Expression Trees: SymPy represents mathematical formulas as Abstract Syntax Trees (AST).
  Evaluating or traversing this tree takes O(N) time, where N is the number of nodes.
- Simplification: The problem of finding the "simplest" form of an expression is 
  computationally undecidable in general (Richardson's theorem). Specific algorithms 
  (like polynomial factorization or simplification) often run in exponential or NP-hard time.
- Calculus (Integration): The Risch algorithm used for symbolic integration is highly 
  complex and can take significant exponential time for large expressions.
- Matrices: Symbolic determinant calculation scales factorially O(N!) with naive 
  expansion, or polynomially with Bareiss algorithms, but suffers from "intermediate 
  expression swell," leading to huge memory footprints.

Real-World Applications:
- Physics & Mechanics: Deriving Lagrangian/Hamiltonian equations of motion.
- Robotics: Computing inverse kinematics and Jacobians symbolically.
- Deep Learning: Generating foundations for automatic differentiation (Autograd).
- Cryptography: Number theory algorithms and modular polynomial arithmetic.
"""

import time
import sympy as sp
from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from typing import List, Dict, Any, Tuple, Union


# =============================================================================
# 1. CORE SYMBOLIC CONCEPTS & EXPRESSIONS
# =============================================================================

def symbolic_basics() -> None:
    """
    Demonstrates the fundamental usage of SymPy:
    - Symbol creation
    - Expression formation
    - Substitution and evaluation
    """
    print("--- 1. Symbolic Basics ---")
    
    # 1. Defining Symbols
    # We define variables x, y, z which will act as algebraic symbols.
    x, y, z = sp.symbols('x y z')
    
    # 2. Creating an expression
    # expr = x^2 + 2x + 1
    expr = x**2 + 2*x + 1
    print(f"Expression: {expr}")
    
    # 3. Factoring and Expanding
    # Factoring converts sum of terms into products
    factored_expr = sp.factor(expr)
    print(f"Factored: {factored_expr}")
    
    # Expanding converts products into sums of terms
    expanded_expr = sp.expand(factored_expr * y)
    print(f"Expanded with 'y': {expanded_expr}")
    
    # 4. Substitution
    # We can substitute x with a numerical value or another symbol
    expr_sub = expr.subs(x, 5)
    print(f"Expression evaluated at x=5: {expr_sub}")
    
    # Substitute x with y^2
    expr_sub_sym = expr.subs(x, y**2)
    print(f"Expression with x substituted by y^2: {expr_sub_sym}")
    
    # 5. Exact Arithmetic vs Floating Point
    # Exact square root
    exact_val = sp.sqrt(8)
    print(f"Exact sqrt(8): {exact_val}")
    
    # Floating point evaluation using .evalf()
    float_val = exact_val.evalf(5)  # 5 digits of precision
    print(f"Numerical eval (5 digits): {float_val}")
    print()


# =============================================================================
# 2. ADVANCED EXPRESSION MANIPULATION (SIMPLIFICATION)
# =============================================================================

def expression_manipulation() -> None:
    """
    Shows how to manipulate and simplify complex expressions.
    Simplification relies on deep algebraic algorithms.
    """
    print("--- 2. Expression Manipulation & Simplification ---")
    
    x, y = sp.symbols('x y')
    
    # Trigonometric Simplification
    # sin^2(x) + cos^2(x) = 1
    trig_expr = sp.sin(x)**2 + sp.cos(x)**2
    simplified_trig = sp.simplify(trig_expr)
    print(f"Original Trig: {trig_expr} => Simplified: {simplified_trig}")
    
    # Rational Function Simplification (Cancel)
    # (x^2 - 1) / (x - 1) => x + 1
    rational_expr = (x**2 - 1) / (x - 1)
    simplified_rational = sp.cancel(rational_expr)
    print(f"Original Rational: {rational_expr} => Cancelled: {simplified_rational}")
    
    # Partial Fraction Decomposition (Apart)
    # 1 / (x^2 - 1) => 1/(2*(x-1)) - 1/(2*(x+1))
    fraction_expr = 1 / (x**2 - 1)
    partial_frac = sp.apart(fraction_expr)
    print(f"Original Fraction: {fraction_expr} => Partial Fractions: {partial_frac}")
    print()


# =============================================================================
# 3. CALCULUS: LIMITS, DERIVATIVES, INTEGRALS, SERIES
# =============================================================================

def calculus_operations() -> None:
    """
    Demonstrates SymPy's powerful calculus capabilities.
    These are operations that normally require human algebraic derivation.
    """
    print("--- 3. Calculus Operations ---")
    
    x, y = sp.symbols('x y')
    
    # 1. Limits
    # limit(sin(x)/x, x->0) = 1
    limit_expr = sp.sin(x) / x
    limit_result = sp.limit(limit_expr, x, 0)
    print(f"Limit of {limit_expr} as x->0: {limit_result}")
    
    # Limit at infinity
    # limit((1 + 1/x)^x, x->oo) = e
    euler_limit = sp.limit((1 + 1/x)**x, x, sp.oo)
    print(f"Limit of (1+1/x)^x as x->oo: {euler_limit}")
    
    # 2. Derivatives (Differentiation)
    # d/dx (e^x * sin(x))
    deriv_expr = sp.exp(x) * sp.sin(x)
    derivative = sp.diff(deriv_expr, x)
    print(f"First derivative of {deriv_expr}: {derivative}")
    
    # Partial derivatives
    multivar_expr = sp.exp(x*y) * sp.cos(x)
    partial_y = sp.diff(multivar_expr, y)
    print(f"Partial derivative w.r.t y of {multivar_expr}: {partial_y}")
    
    # 3. Integrals (Integration)
    # Indefinite integral: int(x^2 * e^x dx)
    integrand = x**2 * sp.exp(x)
    indef_integral = sp.integrate(integrand, x)
    print(f"Indefinite integral of {integrand}: {indef_integral}")
    
    # Definite integral: int_0^pi sin(x) dx = 2
    def_integral = sp.integrate(sp.sin(x), (x, 0, sp.pi))
    print(f"Definite integral of sin(x) from 0 to pi: {def_integral}")
    
    # 4. Taylor Series Expansion
    # Series of e^x around x=0 up to 5th order
    series_exp = sp.series(sp.exp(x), x, 0, 5)
    print(f"Maclaurin series of exp(x) up to O(x^5): {series_exp}")
    print()


# =============================================================================
# 4. SOLVING EQUATIONS & DIFFERENTIAL EQUATIONS
# =============================================================================

def solving_equations() -> None:
    """
    Solving algebraic equations, linear systems, and ODEs (Ordinary 
    Differential Equations).
    """
    print("--- 4. Solving Equations ---")
    
    x, y, z = sp.symbols('x y z')
    
    # 1. Algebraic Equations
    # solve assumes the expression equals 0: x^2 - 4 = 0
    quad_eq = x**2 - 4
    solutions = sp.solve(quad_eq, x)
    print(f"Solutions to {quad_eq} = 0: {solutions}")
    
    # Solving for a specific variable in a multivariate equation
    # x + y + z = 1 => solve for x
    multivar_eq = sp.Eq(x + y + z, 1)
    sol_x = sp.solve(multivar_eq, x)
    print(f"Solving {multivar_eq} for x: {sol_x}")
    
    # 2. System of Linear Equations
    # x + y = 3
    # x - y = 1
    # Solution: x=2, y=1
    eq1 = sp.Eq(x + y, 3)
    eq2 = sp.Eq(x - y, 1)
    sys_sol = sp.solve((eq1, eq2), (x, y))
    print(f"Solution to system [x+y=3, x-y=1]: {sys_sol}")
    
    # 3. Ordinary Differential Equations (ODEs)
    print("\n-- Ordinary Differential Equations --")
    # Define an undefined function f(x)
    f = sp.Function('f')
    
    # Define the ODE: f''(x) - 2f'(x) + f(x) = sp.sin(x)
    ode = sp.Eq(f(x).diff(x, x) - 2*f(x).diff(x) + f(x), sp.sin(x))
    print(f"ODE: {ode}")
    
    # Solve the ODE (dsolve)
    ode_sol = sp.dsolve(ode, f(x))
    print(f"General Solution: {ode_sol}")
    print()


# =============================================================================
# 5. SYMBOLIC LINEAR ALGEBRA
# =============================================================================

def symbolic_linear_algebra() -> None:
    """
    Demonstrates working with Matrices containing symbolic elements.
    Warning: Symbolic matrix operations suffer from intermediate expression swell.
    """
    print("--- 5. Symbolic Linear Algebra ---")
    
    x, y = sp.symbols('x y')
    
    # Create a 2x2 Symbolic Matrix
    M = sp.Matrix([
        [1, x],
        [y, 1]
    ])
    
    print(f"Matrix M:\n{M}")
    
    # Determinant
    det_M = M.det()
    print(f"Determinant of M: {det_M}")
    
    # Matrix Inversion
    # Inverses involve dividing by the determinant.
    try:
        M_inv = M.inv()
        print(f"Inverse of M:\n{M_inv}")
    except sp.NonInvertibleMatrixError:
        print("Matrix is not invertible for all values.")
        
    # Eigenvalues and Eigenvectors
    # Let's use a numerical matrix for cleaner output, but solved symbolically
    A = sp.Matrix([
        [3, 2],
        [1, 4]
    ])
    eigenvals = A.eigenvals()
    print(f"Eigenvalues of [[3,2],[1,4]]: {eigenvals}")  # Dictionary {eigenvalue: algebraic_multiplicity}
    print()


# =============================================================================
# 6. REAL-WORLD APPLICATION: KINEMATICS (PROJECTILE MOTION)
# =============================================================================

def application_kinematics() -> None:
    """
    Real-World Scenario: Deriving the trajectory equation of a projectile.
    
    We start with basic Newtonian mechanics:
    a_x(t) = 0
    a_y(t) = -g
    
    We integrate to find velocity, and integrate again to find position.
    Then we eliminate time 't' to find y(x), the parabolic trajectory.
    """
    print("--- 6. Real-World Application: Kinematics ---")
    
    # Define symbols
    t, v0, theta, g, x0, y0 = sp.symbols('t v_0 theta g x_0 y_0', real=True, positive=True)
    
    # Accelerations
    a_x = 0
    a_y = -g
    
    # Integrating to get velocities (v = int(a) + v_init)
    # v0_x = v0 * cos(theta), v0_y = v0 * sin(theta)
    v_x = sp.integrate(a_x, t) + v0 * sp.cos(theta)
    v_y = sp.integrate(a_y, t) + v0 * sp.sin(theta)
    
    print(f"Velocity X: {v_x}")
    print(f"Velocity Y: {v_y}")
    
    # Integrating to get positions (r = int(v) + r_init)
    x_t = sp.integrate(v_x, t) + x0
    y_t = sp.integrate(v_y, t) + y0
    
    print(f"Position X(t): {x_t}")
    print(f"Position Y(t): {y_t}")
    
    # Eliminate 't' to find trajectory y(x)
    # 1. Solve x(t) = x for t (assuming x0 = 0)
    x = sp.symbols('x')
    x_t_eq = sp.Eq(x_t.subs(x0, 0), x)
    t_sol = sp.solve(x_t_eq, t)[0]  # Get the expression for t
    print(f"Time 't' in terms of 'x': {t_sol}")
    
    # 2. Substitute t into y(t)
    y_x = y_t.subs(t, t_sol).subs(y0, 0)
    
    # Simplify using trigonometric identities
    y_x_simplified = sp.simplify(y_x)
    y_x_trig = sp.trigsimp(y_x_simplified)
    
    print(f"Trajectory Equation y(x) [Assuming x0=0, y0=0]:")
    print(f"y(x) = {y_x_trig}")
    print("Notice this represents a classic inverted parabola: y = x*tan(theta) - g*x^2 / (2*v0^2*cos^2(theta))")
    print()


# =============================================================================
# 7. INTERVIEW CHALLENGE: SYMBOLIC MACLAURIN COEFFICIENTS
# =============================================================================

def interview_challenge(expr: Expr, var: Symbol, n_terms: int) -> List[Expr]:
    """
    Challenge: Without using the built-in `series` method, write a function 
    that computes the first N Maclaurin series coefficients (Taylor series 
    at x=0) for a given symbolic expression.
    
    Formula: c_n = f^(n)(0) / n!
    where f^(n) is the nth derivative of f(x).
    
    Args:
        expr: The SymPy expression f(x).
        var: The symbolic variable x.
        n_terms: The number of terms to compute (0 to n_terms-1).
        
    Returns:
        List of coefficients c_n.
    """
    print(f"--- Interview Challenge: Maclaurin Coefficients ---")
    coefficients = []
    
    # Start with the 0-th derivative (the function itself)
    current_deriv = expr
    
    for n in range(n_terms):
        # Evaluate derivative at var = 0
        val_at_zero = current_deriv.subs(var, 0)
        
        # Calculate coefficient: val / n!
        coeff = val_at_zero / math.factorial(n)
        coefficients.append(coeff)
        
        # Calculate the next derivative for the next iteration
        current_deriv = sp.diff(current_deriv, var)
        
    return coefficients


# =============================================================================
# 8. PERFORMANCE ANALYSIS: NUMERICAL VS SYMBOLIC
# =============================================================================

def analyze_performance() -> None:
    """
    Compares the execution time of symbolic evaluation vs numerical execution.
    """
    print("--- Performance Analysis: Symbolic vs Numerical ---")
    import math as math_module
    
    x = sp.symbols('x')
    sym_expr = sp.sin(x)**2 + sp.cos(x)**2
    
    # 1. Symbolic substitution and evaluation
    start = time.perf_counter()
    for i in range(1000):
        _ = sym_expr.subs(x, i).evalf()
    sym_time = time.perf_counter() - start
    
    # 2. Native Python numerical evaluation
    start = time.perf_counter()
    for i in range(1000):
        _ = math_module.sin(i)**2 + math_module.cos(i)**2
    num_time = time.perf_counter() - start
    
    print(f"Symbolic Evaluation (1000 iter): {sym_time:.4f} sec")
    print(f"Numerical Evaluation (1000 iter): {num_time:.4f} sec")
    print(f"Ratio (Symbolic/Numerical): ~{sym_time/num_time:.0f}x slower")
    print("\nConclusion: SymPy is for exact algebraic derivation, NOT for fast numerical number-crunching in loops.")
    print("Use SymPy to find the exact formula, then use `sympy.lambdify` to convert it to a fast NumPy/math function for iteration.")
    print()


# =============================================================================
# 9. UNIT TESTS
# =============================================================================

def run_tests() -> None:
    """
    Test suite to validate our implementations and custom challenge.
    """
    print("--- Running Tests ---")
    
    x = sp.symbols('x')
    
    # Test 1: Limit validation
    assert sp.limit(sp.sin(x)/x, x, 0) == 1, "Limit test failed"
    
    # Test 2: Derivative validation
    assert sp.diff(x**2, x) == 2*x, "Derivative test failed"
    
    # Test 3: Interview Challenge (Maclaurin coefficients for e^x)
    # e^x coefficients: 1, 1, 1/2, 1/6, 1/24...
    coeffs = interview_challenge(sp.exp(x), x, 5)
    expected_coeffs = [1, 1, sp.Rational(1, 2), sp.Rational(1, 6), sp.Rational(1, 24)]
    assert coeffs == expected_coeffs, f"Interview challenge failed. Expected {expected_coeffs}, got {coeffs}"
    print(f"Maclaurin coefficients of exp(x) up to n=4: {coeffs}")
    
    # Test 4: Interview Challenge (Maclaurin coefficients for sin(x))
    # sin(x) coefficients: 0, 1, 0, -1/6, 0...
    coeffs_sin = interview_challenge(sp.sin(x), x, 5)
    expected_coeffs_sin = [0, 1, 0, sp.Rational(-1, 6), 0]
    assert coeffs_sin == expected_coeffs_sin, "Interview challenge failed for sin(x)"
    print(f"Maclaurin coefficients of sin(x) up to n=4: {coeffs_sin}")
    
    print("All tests passed successfully!\n")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print(f"{'='*60}")
    print(f"========== Exploring {'SymPy Symbolic Math'.upper()} ==========")
    print(f"{'='*60}\n")
    
    symbolic_basics()
    expression_manipulation()
    calculus_operations()
    solving_equations()
    symbolic_linear_algebra()
    application_kinematics()
    
    # Interview challenge is called inside run_tests, but let's demo it here too.
    x = sp.symbols('x')
    print("Demo Interview Challenge for cos(x):")
    demo_coeffs = interview_challenge(sp.cos(x), x, 6)
    print(f"cos(x) coeffs (n=0 to 5): {demo_coeffs}\n")
    
    analyze_performance()
    run_tests()
    
    print(f"{'='*60}")
    print(f"========== END OF {'SymPy Symbolic Math'.upper()} ==========")
    print(f"{'='*60}\n")
